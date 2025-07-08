import io
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db import transaction
from django.db.models import Prefetch
from django.http import JsonResponse
from users.models import UserAccount
from .models import Modulo, Dimensao, Pergunta, RespostaDimensao, RespostaModulo
from django.shortcuts import get_object_or_404
import json
import matplotlib.pyplot as plt
import numpy as np
from reportlab.lib.utils import ImageReader


class QuestionarioView(APIView):

    def get(self, request):
        try:
            usuario = request.user if request.user.is_authenticated else None
            porte_usuario = None
            if usuario and hasattr(usuario, "porte"):
                porte_usuario = usuario.porte

            modulos = Modulo.objects.prefetch_related(
                'dimensoes__perguntas').all()

            dadosQuestionario = []

            for modulo in modulos:
                dimensoesDoModulo = modulo.dimensoes.all()
                dadosDimensoes = []

                for dimensao in dimensoesDoModulo:

                    perguntasData = []
                    for p in perguntas_qs:
                        perguntasData.append({
                            'id': p.id,
                            'pergunta': p.pergunta,
                        })

                    dadosDimensao = {
                        'dimensaoTitulo': dimensao.titulo,
                        'descricao': dimensao.descricao,
                        'explicacao': dimensao.explicacao,
                        'perguntas': perguntasData
                    }
                    dadosDimensoes.append(dadosDimensao)

                dadosModulo = {
                    'nome': modulo.nome,
                    'descricao': modulo.descricao,
                    'tempo': modulo.tempo,
                    'perguntasQntd': modulo.perguntasQntd,
                    'dimensoes': dadosDimensoes
                }
                dadosQuestionario.append(dadosModulo)

            return Response({'modulos': dadosQuestionario})

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ModuloView(APIView):

    def get(self, request, nomeModulo):
        try:

            usuario = request.user if request.user.is_authenticated else None
            porte_usuario = None
            if usuario and hasattr(usuario, "porte"):
                porte_usuario = usuario.porte


            perguntas_queryset = Pergunta.objects.all()
            if porte_usuario == "MEI":
                perguntas_queryset = perguntas_queryset.exclude(exclusao='MEI')

            prefetch_dimensoes_com_perguntas_filtradas = Prefetch(
                'dimensoes',  # O campo a ser pré-buscado no modelo Modulo
                queryset=Dimensao.objects.prefetch_related(
                    Prefetch(
                        'perguntas',  # O campo a ser pré-buscado no modelo Dimensao
                        queryset=perguntas_queryset,
                        to_attr='perguntas_filtradas'  # Armazena o resultado filtrado aqui
                    )
                )
            )

            moduloObj = get_object_or_404(
                Modulo.objects.prefetch_related(prefetch_dimensoes_com_perguntas_filtradas),
                nome=nomeModulo
            )

            dadosDimensoes = []

            for dimensao in moduloObj.dimensoes.all():
                perguntasData = []
                if hasattr(dimensao, 'perguntas_filtradas'):
                        for p in dimensao.perguntas_filtradas:
                            perguntasData.append({
                                'id': p.id,
                                'pergunta': p.pergunta,
                            })

                if perguntasData:
                    dados_dimensao = {
                        'dimensaoTitulo': dimensao.titulo,
                        'descricao': dimensao.descricao,
                        'explicacao': dimensao.explicacao,
                        'perguntas': perguntasData,
                    }
                    dadosDimensoes.append(dados_dimensao)

            response_data = {
                'nomeModulo': moduloObj.nome,
                'dimensoes': dadosDimensoes
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': f'Ocorreu um erro interno no servidor: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SalvarRespostasModuloView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, nomeModulo):
        usuario = request.user
        try:
            modulo = get_object_or_404(Modulo, nome=nomeModulo)
        except Modulo.DoesNotExist:
            return Response(
                {'error': f'Módulo com nome "{nomeModulo}" não encontrado.'},
                status=status.HTTP_404_NOT_FOUND
            )

        respostasData = request.data.get('respostas')

        if respostasData is None:
            return Response(
                {'error': 'Payload deve conter a chave "respostas".'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not isinstance(respostasData, list):
            return Response(
                {'error': '"respostas" deve ser uma lista.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not respostasData:
            return Response(
                {'warning': 'A lista "respostas" está vazia. Nenhuma resposta foi processada.'},
                status=status.HTTP_200_OK
            )

        erros = []
        perguntasRespondidasId = set()
        somasPorDimensao = {}

        try:
            perguntasDoModulo = Pergunta.objects.filter(
                dimensao__modulo=modulo
            ).select_related('dimensao')
            mapa_perguntas_validas = {p.id: p for p in perguntasDoModulo}
        except Exception as e:
            return Response(
                {'error': f'Erro crítico ao buscar perguntas do módulo: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        for idx, resposta_info in enumerate(respostasData):
            if not isinstance(resposta_info, dict):
                erros.append(f"Item {idx+1}: Não é um objeto JSON válido.")
                continue

            perguntaId = resposta_info.get('perguntaId')
            valor = resposta_info.get('valor')

            if perguntaId is None:
                erros.append(f"Item {idx+1}: Chave 'perguntaId' ausente.")
                continue
            if valor is None:
                erros.append(
                    f"Item {idx+1} (Pergunta ID {perguntaId}): Chave 'valor' ausente.")
                continue

            try:
                valor_int = int(valor)
            except (ValueError, TypeError):
                erros.append(
                    f"Item {idx+1} (Pergunta ID {perguntaId}): 'valor' deve ser um número inteiro (recebeu '{valor}').")
                continue

            perguntaObj = mapa_perguntas_validas.get(perguntaId)
            if not perguntaObj:
                erros.append(
                    f"Item {idx+1}: Pergunta com ID {perguntaId} não encontrada ou não pertence ao módulo '{nomeModulo}'.")
                continue

            if perguntaId in perguntasRespondidasId:
                erros.append(
                    f"Item {idx+1}: Resposta duplicada para a pergunta com ID {perguntaId} nesta requisição.")
                continue
            perguntasRespondidasId.add(perguntaId)

            dimensaoObj = perguntaObj.dimensao
            dimensaoPk = dimensaoObj.pk
            valorPonderado = valor_int * perguntaObj.peso
            somasPorDimensao[dimensaoPk] = somasPorDimensao.get(
                dimensaoPk, 0) + valorPonderado

        if erros:
            return Response({
                'error': 'Falha na validação das respostas. Nenhuma resposta foi salva.',
                'detalhes': erros,
            }, status=status.HTTP_400_BAD_REQUEST)

        dimensoesAtualizadas = []
        respostaModuloStatus = None
        valorFinalModulo = 0

        try:
            for dimensaoPk, somaTotal in somasPorDimensao.items():
                respostaDimensaoObj, created = RespostaDimensao.objects.update_or_create(
                    usuario=usuario,
                    dimensao_id=dimensaoPk,
                    defaults={'valorFinal': somaTotal}
                )
                dimensoesAtualizadas.append({
                    'dimensaoId': dimensaoPk,
                    'tituloDimensao': respostaDimensaoObj.dimensao.titulo,
                    'valorFinal': somaTotal,
                    'status': 'Criada' if created else 'Atualizada'
                })

            valorFinalModulo = sum(somasPorDimensao.values())

            respostaModuloObj, created_modulo = RespostaModulo.objects.update_or_create(
                usuario=usuario,
                modulo=modulo,
                defaults={'valorFinal': valorFinalModulo}
            )
            respostaModuloStatus = 'Criada' if created_modulo else 'Atualizada'

        except Exception as e:
            return Response(
                {'error': f'Erro ao salvar respostas no banco de dados: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            {
                'message': f'Respostas para o módulo "{nomeModulo}" processadas e salvas com sucesso.',
                'modulo': {
                    'moduloId': modulo.id,
                    'nomeModulo': modulo.nome,
                    'valorFinal': valorFinalModulo,
                    'status': respostaModuloStatus
                },
                'dimensoesAtualizadas': dimensoesAtualizadas
            },
            status=status.HTTP_200_OK
        )

class GerarRelatorioModuloView(APIView):
    permission_classes = [IsAuthenticated]

    def _avaliar_modulo(self, pontuacao):
        if 3201 <= pontuacao <= 4000:
            return "Excelente"
        elif 2401 <= pontuacao <= 3200:
            return "Suficiente"
        elif 1601 <= pontuacao <= 2400:
            return "Neutro"
        elif 800 <= pontuacao <= 1600:
            return "Insuficiente"
        else:
            return "Fora da faixa de avaliação"

    def _avaliar_dimensao(self, pontuacao):
        if 401 <= pontuacao <= 500:
            return "Excelente"
        elif 301 <= pontuacao <= 400:
            return "Suficiente"
        elif 201 <= pontuacao <= 300:
            return "Neutro"
        elif 100 <= pontuacao <= 200:
            return "Insuficiente"
        else:
            return "Fora da faixa de avaliação"

    def get(self, request, nomeModulo):
        usuario = request.user

        try:
            modulo = get_object_or_404(Modulo, nome=nomeModulo)

            resposta_modulo = get_object_or_404(
                RespostaModulo, usuario=usuario, modulo=modulo
            )

            respostas_dimensoes = RespostaDimensao.objects.filter(
                usuario=usuario,
                dimensao__modulo=modulo
            ).select_related('dimensao').order_by('dimensao__id')

            if not respostas_dimensoes.exists():
                 return Response(
                     {'error': f'Respostas das dimensões para o módulo "{nomeModulo}" não encontradas para este usuário.'},
                     status=status.HTTP_404_NOT_FOUND
                 )

            buffer = io.BytesIO()
            c = canvas.Canvas(buffer, pagesize=A4)
            styles = getSampleStyleSheet()
            width, height = A4

            y_position = height - 1.5*cm
            margin_left = 1.5*cm
            content_width = width - 2*margin_left

            style_title = styles['h1']
            style_h2 = styles['h2']
            style_body = styles['BodyText']
            style_body.leading = 14

            p = Paragraph("Relatório de Desempenho", style_title)
            p.wrapOn(c, content_width, height)
            p_height = p.height
            p.drawOn(c, margin_left, y_position - p_height)
            y_position -= (p_height + 0.5*cm)

            p = Paragraph(f"<b>Usuário:</b> {usuario.username} ({usuario.email})", style_body)
            p.wrapOn(c, content_width, height)
            p_height = p.height
            p.drawOn(c, margin_left, y_position - p_height)
            y_position -= (p_height + 0.1*cm)

            porte_empresa = getattr(usuario, 'porte', 'Não informado')
            p = Paragraph(f"<b>Porte da Empresa:</b> {porte_empresa}", style_body)
            p.wrapOn(c, content_width, height)
            p_height = p.height
            p.drawOn(c, margin_left, y_position - p_height)
            y_position -= (p_height + 0.1*cm)

            setor_empresa = getattr(usuario, 'setor', 'Não informado')
            p = Paragraph(f"<b>Setor de Atuação:</b> {setor_empresa}", style_body)
            p.wrapOn(c, content_width, height)
            p_height = p.height
            p.drawOn(c, margin_left, y_position - p_height)
            y_position -= (p_height + 0.5*cm)

            p = Paragraph(f"<b>Módulo:</b> {modulo.nome}", style_h2)
            p.wrapOn(c, content_width, height)
            p_height = p.height
            p.drawOn(c, margin_left, y_position - p_height)
            y_position -= (p_height + 0.1*cm)

            p = Paragraph(f"<i>Descrição:</i> {modulo.descricao}", style_body)
            p.wrapOn(c, content_width, height)
            p_height = p.height
            p.drawOn(c, margin_left, y_position - p_height)
            y_position -= (p_height + 0.5*cm)

            pontuacao_modulo = resposta_modulo.valorFinal
            avaliacao_modulo = self._avaliar_modulo(pontuacao_modulo)
            p = Paragraph(f"<b>Resultado Geral do Módulo:</b> {pontuacao_modulo} pontos - <b>{avaliacao_modulo}</b>", style_body)
            p.wrapOn(c, content_width, height)
            p_height = p.height
            p.drawOn(c, margin_left, y_position - p_height)
            y_position -= (p_height + 0.7*cm)

            p = Paragraph("Resultados por Dimensão:", style_h2)
            p.wrapOn(c, content_width, height)
            p_height = p.height
            p.drawOn(c, margin_left, y_position - p_height)
            y_position -= (p_height + 0.3*cm)

            for resp_dim in respostas_dimensoes:
                dimensao = resp_dim.dimensao
                pontuacao_dimensao = resp_dim.valorFinal
                avaliacao_dimensao = self._avaliar_dimensao(pontuacao_dimensao)

                p = Paragraph(f"<b>{dimensao.titulo}:</b>", style_body)
                p.wrapOn(c, content_width, height)
                p_height = p.height
                p.drawOn(c, margin_left, y_position - p_height)
                y_position -= p_height

                p = Paragraph(f"    Pontuação: {pontuacao_dimensao} - <b>{avaliacao_dimensao}</b>", style_body)
                p.wrapOn(c, content_width, height)
                p_height = p.height
                p.drawOn(c, margin_left, y_position - p_height)
                y_position -= (p_height + 0.3*cm)

                if y_position < 3*cm:
                    c.showPage() 
                    y_position = height - 1.5*cm

            img_width = 17 * cm
            img_height =10 * cm
            x_center = (width - img_width) / 2  # Centraliza na página
            if y_position - img_height < 2*cm:
                c.showPage()
                y_position = height - 2*cm

            labels = [resp.dimensao.titulo for resp in respostas_dimensoes]
            values = [resp.valorFinal for resp in respostas_dimensoes]
            if not labels:
                labels = ['Sem dados']
                values = [0]

            if setor_empresa == 'Setor A':
                valores_comparacao = [200 for _ in labels]
            elif setor_empresa == 'Setor B':
                valores_comparacao = [300 for _ in labels]
            else:
                valores_comparacao = [400 for _ in labels]

            x = np.arange(len(labels))  # posições das barras
            width = 0.35  # largura das barras

            fig, ax = plt.subplots(figsize=(10, 5))
            rects1 = ax.bar(x - width/2, values, width, label='Seu resultado', color='#4bd360')
            rects2 = ax.bar(x + width/2, valores_comparacao, width, label=('Média do ' + setor_empresa), color='#ec5353')

            ax.set_ylabel('Pontuação')
            ax.set_title('Desempenho')
            ax.set_xticks(x)
            ax.set_xticklabels(labels, rotation=20, ha='right')
            ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
            plt.tight_layout()

            # Adiciona valores acima das barras
            for rect in rects1 + rects2:
                height = rect.get_height()
                ax.annotate(f'{int(height)}',
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom', fontsize=8)

            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='PNG', bbox_inches='tight', dpi=120)
            plt.close(fig)
            img_buffer.seek(0)
            col_img = ImageReader(img_buffer)

            c.drawImage(col_img, x_center, y_position - img_height, width=img_width, height=img_height)
            y_position -= (img_height + 0.5*cm)

            c.save()

            buffer.seek(0)
            response = HttpResponse(buffer, content_type='application/pdf')
            filename = f"relatorio_{nomeModulo.replace(' ', '_')}_{usuario.username}.pdf"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'

            return response

        except Modulo.DoesNotExist:
            return Response(
                {'error': f'Módulo com nome "{nomeModulo}" não encontrado.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except RespostaModulo.DoesNotExist:
             return Response(
                {'error': f'O usuário {usuario.username} ainda não respondeu ao módulo "{nomeModulo}".'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Erro ao gerar o relatório PDF: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )