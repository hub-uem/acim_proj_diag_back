
INSERT INTO questionario_modulo (nome, perguntasQntd, descricao, tempo) VALUES
('Diagnóstico Organizacional', 54, 'O Diagnóstico Organizacional é uma ferramenta essencial para entender a saúde da sua empresa. Ele ajuda a identificar pontos fortes e áreas que precisam de melhorias, permitindo que você tome decisões informadas para o futuro do seu negócio.', 40);

INSERT INTO questionario_dimensao (titulo, descricao, modulo_id, explicacao) VALUES
('Estratégia', 'Avalie as questões referentes à ESTRATÉGIA da sua empresa, indicando em uma escala de concordância de 1 a 5 onde 1 significa discordo totalmente e 5 significa concordo totalmente.', 1, 'Explicacao'),
('Jurídico e Riscos', 'Avalie as questões referentes à JURÍDICO E RISCOS da sua empresa, indicando em uma escala de concordância de 1 a 5 onde 1 significa discordo totalmente e 5 significa concordo totalmente.', 1, 'Explicacao'),
('Governança', 'Avalie as questões referentes à GOVERNANÇA da sua empresa, indicando em uma escala de concordância de 1 a 5 onde 1 significa discordo totalmente e 5 significa concordo totalmente.', 1, 'Explicacao'),
('Finanças', 'Avalie as questões referentes à FINANÇAS da sua empresa, indicando em uma escala de concordância de 1 a 5 onde 1 significa discordo totalmente e 5 significa concordo totalmente.', 1, 'Explicacao'),
('Inovação e TI', 'Avalie as questões referentes às políticas INOVAÇÃO E TI da sua empresa, indicando em uma escala de concordância de 1 a 5 onde 1 significa discordo totalmente e 5 significa concordo totalmente.', 1, 'Explicacao'),
('Operações e Processos', 'Avalie as questões referentes à OPERAÇÕES E PROCESSOS da sua empresa, indicando em uma escala de concordância de 1 a 5 onde 1 significa discordo totalmente e 5 significa concordo totalmente.', 1, 'Explicacao'),
('Marketing e Vendas', 'Avalie as questões referentes à MARKETING E VENDAS da sua empresa, indicando em uma escala de concordância de 1 a 5 onde 1 significa discordo totalmente e 5 significa concordo totalmente.', 1, 'Explicacao'),
('RH', 'Avalie as questões referentes à RH da sua empresa, indicando em uma escala de concordância de 1 a 5 onde 1 significa discordo totalmente e 5 significa concordo totalmente.', 1, 'Explicacao');

INSERT INTO questionario_pergunta (pergunta, dimensao_id, peso, exclusao) VALUES
('Minha empresa possui planos de ação com prazos definidos e responsáveis designados para alcançar as metas.', 1, 17, 'NENHUM'),
('Minha empresa monitora os resultados e metas de forma periódica e sistemática.', 1, 17, 'NENHUM'),
('Minha empresa possui uma visão clara de onde quer chegar nos próximos anos.', 1, 15, 'NENHUM'),
('Minha empresa e toda a equipe seguem consistentemente seus pilares estratégicos (missão, visão e valores).', 1, 10, 'MEI'),
('Minha empresa define e comunica claramente seus objetivos estratégicos para toda a equipe.', 1, 13, 'NENHUM'),
('Os colaboradores da minha empresa entendem como seu trabalho contribui para os objetivos estratégicos.', 1, 15, 'MEI'),
('Os valores e a cultura organizacional da minha empresa são reforçados e praticados no dia a dia.', 1, 13, 'MEI'),

('Minha empresa possui uma avaliação atualizada do seu passivo trabalhista, cível e tributário.', 2, 20, 'NENHUM'),
('Minha empresa toma todas as medidas jurídicas necessárias para reduzir a inadimplência.', 2, 15, 'NENHUM'),
('Minha empresa responde às notificações do Procon e possui controle sobre sua frequência.', 2, 15, 'MEI'),
('Minha empresa possui uma avaliação formal quanto à existência ou não de passivo ambiental.', 2, 15, 'MEI'),
('As licenças municipais, estaduais e federais da minha empresa estão em ordem e foram avaliadas pelo setor jurídico.', 2, 20, 'MEI'),
('Minha empresa realizou o alinhamento necessário para aplicar a NR 1, bem como implantou a NR 17.', 2, 15, 'MEI'),

('Minha empresa possui mecanismos formais de tomada de decisão que garantem transparência e responsabilização.', 3, 20, 'MEI'),
('Minha empresa possui uma estrutura de governança bem definida, com papéis e responsabilidades claros para os líderes.', 3, 18, 'MEI'),
('Minha empresa identifica, avalia e monitora regularmente os riscos e passivos financeiros e trabalhistas.', 3, 18, 'MEI'),
('Minha empresa conta com um profissional ou escritório jurídico para apoiar em decisões estratégicas e operacionais.', 3, 10, 'MEI'),
('Os contratos e documentos jurídicos da minha empresa são revisados periodicamente para garantir conformidade e reduzir riscos.', 3, 14, 'MEI'),
('Minha empresa adota medidas preventivas para evitar fraudes, corrupção e outros riscos organizacionais.', 3, 20, 'MEI'),

('Minha empresa analisa seus demonstrativos financeiros (DRE, Balanço Patrimonial etc.) de forma constante.', 4, 13, 'NENHUM'),
('Minha empresa possui controles financeiros básicos, como caixa, bancos, estoques, contas a pagar e receber, e custos.', 4, 17, 'NENHUM'),
('Minha empresa separa de forma rigorosa as finanças da pessoa jurídica e da pessoa física.', 4, 10, 'NENHUM'),
('Minha empresa realiza planejamento financeiro com base em dados passados, atuais e projeções futuras.', 4, 12, 'NENHUM'),
('Minha empresa possui métodos eficazes para apurar seus resultados e mensurar o lucro mensal com precisão.', 4, 13, 'NENHUM'),
('Minha empresa possui controle detalhado do seu fluxo de caixa.', 4, 15, 'NENHUM'),
('Minha empresa mantém reservas de emergência e faz provisionamentos para lidar com imprevistos financeiros.', 4, 8, 'NENHUM'),
('Minha empresa precifica seus produtos ou serviços com base em dados financeiros como custos, margens e contribuições.', 4, 12, 'NENHUM'),

('Minha empresa possui uma estratégia clara para inovar e gerar resultados como aumento de vendas, redução de custos ou melhoria na satisfação do cliente.', 5, 28, 'NENHUM'),
('Minha empresa acompanha novas tecnologias (IA, IoT, Blockchain etc.) e se prepara para utilizá-las futuramente.', 5, 23, 'NENHUM'),
('Minha empresa tem um processo organizado para incentivar novas ideias e transformá-las em melhorias com a participação da equipe.', 5, 18, 'NENHUM'),
('Minha empresa ajusta seus produtos e serviços com base nas mudanças nas necessidades dos clientes e nos feedbacks recebidos.', 5, 13, 'NENHUM'),
('Minha empresa busca parcerias com universidades, especialistas ou outras empresas para promover inovação e melhorar seus serviços.', 5, 8, 'NENHUM'),
('Minha empresa adota tecnologias e inovações para escalar o crescimento e ampliar sua presença no mercado.', 5, 5, 'MEI'),
('Minha empresa utiliza tecnologia e inovação para se adaptar ao mercado e melhorar sua eficiência operacional diante de desafios.', 5, 5, 'NENHUM'),

('Minha empresa utiliza sistemas e/ou aplicativos de gestão para cadastrar informações e controlar vendas.', 6, 20, 'NENHUM'),
('Minha empresa registra e trata as reclamações dos clientes de forma sistemática.', 6, 15, 'NENHUM'),
('Minha empresa monitora indicadores operacionais relevantes para sua atividade.', 6, 18, 'NENHUM'),
('Os principais processos do meu negócio são padronizados e possuem controles que garantem sua execução adequada.', 6, 20, 'NENHUM'),
('Minha empresa acompanha a qualidade do trabalho realizado pelos colaboradores.', 6, 17, 'NENHUM'),
('Minha empresa possui rotinas estruturadas de treinamento e capacitação para sua equipe.', 6, 10, 'NENHUM'),

('Minha empresa conhece bem as necessidades e desejos dos seus clientes.', 7, 20, 'NENHUM'),
('Minha empresa utiliza diversos meios de comunicação (online e offline) que são atualizados frequentemente.', 7, 12, 'NENHUM'),
('Minha empresa define claramente seus públicos e aplica segmentações de mercado para suas estratégias.', 7, 15, 'NENHUM'),
('Minha empresa realiza pesquisas e observações de mercado, inclusive sobre concorrentes, para se atualizar e melhorar.', 7, 13, 'NENHUM'),
('Minha empresa realiza ações específicas para fidelizar e manter os clientes atuais.', 7, 15, 'NENHUM'),
('Minha empresa utiliza mecanismos para avaliar a satisfação dos clientes.', 7, 12, 'NENHUM'),
('Minha empresa possui um plano estruturado de divulgação de seus produtos e serviços.', 7, 13, 'NENHUM'),

('Minha empresa fornece treinamentos e orientações para que os colaboradores executem bem suas funções.', 8, 15, 'NENHUM'),
('Após a contratação, os colaboradores da minha empresa recebem treinamentos contínuos para melhorar seu desempenho.', 8, 15, 'NENHUM'),
('Os empresários da minha empresa investem no próprio desenvolvimento gerencial e aplicam o que aprendem na prática.', 8, 13, 'MEI'),
('As funções e responsabilidades das pessoas e equipes da minha empresa estão bem definidas e organizadas.', 8, 15, 'NENHUM'),
('Minha empresa fornece feedbacks estruturados aos funcionários sobre o desempenho do seu trabalho.', 8, 12, 'NENHUM'),
('Minha empresa realiza processos seletivos baseados em critérios e requisitos bem definidos para cada função.', 8, 15, 'MEI'),
('Minha empresa promove ações para melhorar a qualidade de vida, satisfação e engajamento dos colaboradores.', 8, 15, 'MEI');