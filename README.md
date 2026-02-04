Samsung AP Extractor Pro 📱⚙️
O Samsung AP Extractor Pro é uma ferramenta gráfica desenvolvida em Python para simplificar o processo de extração e descompressão de partições de arquivos de firmware da Samsung (geralmente o arquivo AP_xxx.tar.md5).

Ele automatiza a extração do contêiner .tar e a descompressão simultânea do formato .lz4, transformando os arquivos em imagens .img prontas para uso.

✨ Funcionalidades
Interface Gráfica (GUI): Interface moderna com tema escuro (Dark Mode).

Seleção Seletiva: Escolha apenas as partições que deseja extrair (ex: boot.img, recovery.img).

Descompressão LZ4 Integrada: Extrai e descomprime arquivos .img.lz4 em um único passo.

Barra de Progresso: Acompanhamento em tempo real da extração.

Multiplataforma: Compatível com Windows, macOS e Linux.

🚀 Como usar
Pré-requisitos
Python 3.x instalado.

Biblioteca lz4: O script utiliza a biblioteca lz4 para lidar com a descompressão. Instale-a via terminal/prompt:

Bash

pip install lz4
Execução
Baixe o arquivo extractor.py.

Execute o script:

Bash

python extractor.py
Clique em "Selecionar AP (.tar.md5)" e escolha o arquivo de firmware da Samsung.

Marque as partições desejadas na lista.

Clique em "EXTRAIR SELECIONADAS".

Ao final, o programa perguntará se você deseja abrir a pasta AP_TRABALHO/EXTRAIDAS onde os arquivos estarão salvos.

🛠️ Estrutura Técnica
Linguagem: Python 3

Interface: tkinter (TTK para estilização avançada).

Threading: O processo de extração roda em uma thread separada para evitar que a interface trave durante o processamento.

Bibliotecas nativas: os, tarfile, subprocess, platform.

📂 Organização de Arquivos
Ao realizar a extração, o script criará a seguinte estrutura:

Plaintext

pasta_do_script/
├── extractor.py
└── AP_TRABALHO/
    └── EXTRAIDAS/      <-- Seus arquivos .img estarão aqui
✒️ Créditos
Desenvolvido por spacexjr.

Nota: Esta ferramenta foi criada para fins educacionais e de manutenção de software. Certifique-se de ter backup dos seus dados antes de realizar modificações em dispositivos móveis.
