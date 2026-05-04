# 🚢 Desafio de Sistemas Embarcados: Monitoramento de Cargas e Contêineres

👤 **Identificação do Candidato**
* **Nome completo:** André Lucas de Souza Lima
* **GitHub:** <a href='https://github.com/AndreLucas23'>AndreLucas23</a>  

---

## 1️⃣ Visão Geral da Solução

**Objetivo do Projeto:**
O projeto consiste no desenvolvimento de um sistema embarcado de telemetria e segurança logística focado em **Edge Computing**. O objetivo é monitorar, em tempo real, a integridade física de contêineres de carga durante o transporte, detectando impactos severos (quedas, colisões) ou inclinações perigosas (tombamento de carga) decorrentes de manuseio inadequado.

**Funcionamento do Sistema:**
Com um sensor MPU6050 fixado rigidamente à estrutura do contêiner, o sistema realiza leituras contínuas da aceleração (força G de impactos) e do giroscópio (velocidade angular e torção). O processador local calcula a magnitude vetorial dessas forças e compara os resultados com os níveis de tolerância da carga embarcada, classificando o status em três níveis: **OK** (Manuseio Seguro), **PERIGO** (Aviso de Turbulência/Choque Leve) ou **CRÍTICO** (Impacto Grave ou Tombamento).

**Interação do Usuário:**
A operação é totalmente autônoma. Inspetores de carga, estivadores ou operadores de guindaste não precisam acionar comandos; eles realizam a triagem visual no pátio através de duas interfaces alocadas na face externa do contêiner: um Display OLED (exibindo o laudo textual do eixo afetado) e um farol LED RGB (sinalização visual de longa distância).

---

## 2️⃣ Arquitetura do Sistema Embarcado

A arquitetura lógica foi estruturada utilizando **Programação Orientada a Objetos (POO)**. O design isola completamente a aquisição de dados brutos das regras de negócio de logística, utilizando injeção de dependências para o barramento I2C.

**Fluxo Principal e Estrutura Lógica:**
1. **Inicialização (`main.py`):** "Liga" o contêiner, configurando os protocolos de comunicação e instanciando os periféricos.
2. **Laço Contínuo (`app.py`):** Mantém a rotina de vigilância ativa (`while self.running`), consultando os sensores em intervalos controlados.
3. **Processamento Matemático (`sensor_controller.py`):** Converte a telemetria bruta em dados compreensíveis. Esta camada decide se um solavanco de caminhão é ignorável ou se uma queda de guindaste rompeu o limite de segurança, devolvendo um dicionário de status para a aplicação.

---

## 3️⃣ Componentes Utilizados na Simulação

A simulação no Wokwi reproduz a eletrônica embarcada no módulo de rastreamento do contêiner, utilizando os seguintes componentes:

* **Microcontrolador:** Unidade de processamento local que analisa os dados da carga sem depender de nuvem ou sinal GPS/Internet.
* **Sensor MPU6050 (Acelerômetro e Giroscópio):** O "labirinto" do contêiner. Conectado via I2C (SDA 21, SCL 22). Capta a violência mecânica (choques físicos) e mudanças abruptas de ângulo (içamento torto ou deslizamento em navios).
* **Display OLED SSD1306:** Conectado via I2C (SDA 21, SCL 22). Tela de auditoria para fiscais de porto, informando qual anomalia ocorreu (se foi de aceleração ou rotação).
* **LED RGB:** Conectado via PWM (Pinos 25, 26 e 27). Age como um "semáforo" da carga, permitindo que a equipe de transporte saiba rapidamente se a caixa exige inspeção interna.

---

## 4️⃣ Decisões Técnicas Relevantes

* **Cálculo de Magnitude Vetorial:** O `SensorController` não confia em eixos estáticos, aplicando a fórmula $\sqrt{x^2 + y^2 + z^2}$. **Justificativa:** Em logística, não sabemos de qual lado o contêiner vai cair ou colidir. A magnitude vetorial garante que a força do impacto seja registrada independentemente da orientação espacial do choque.
* **Limiares Parametrizados (`config.py`):** As constantes de segurança (ex: `ACCEL_CRITICAL`) foram isoladas. **Justificativa:** Isso permite que o sistema seja facilmente reprogramado dependendo do tipo de frete. Uma carga de algodão terá limiares altíssimos, enquanto uma carga de vidros ou eletrônicos terá limiares críticos rigorosos no mesmo código.
* **Compartilhamento de Barramento (I2C):** O sensor de movimento e o display operam nas mesmas portas. **Justificativa:** Economiza pinos do microcontrolador e demonstra maturidade em arquitetura de hardware multiplexado.
* **Janela de Polling (350ms):** Intervalo definido no laço principal. **Justificativa:** Amostrar dados 3 vezes por segundo é ideal para capturar solavancos físicos, evitando o excesso de processamento (*overhead*) que esgotaria a bateria autônoma do dispositivo ao longo da viagem.

---

## 5️⃣ Resultados Obtidos

O sistema embarcado demonstrou aderência total ao cenário logístico simulado:

* **Detecção Confiável:** Qualquer impacto bruto (aceleração acima da curva de tolerância) ou tombamento severo (giroscópio) foi imediatamente classificado e exibido.
* **Resiliência Anti-Falha:** O bloco `try/except` no arquivo de aplicação garante que, se o MPU6050 sofrer uma desconexão elétrica por uma fração de segundo devido à vibração mecânica intensa, o processador apenas reportará o erro no log de sistema, impedindo que o dispositivo inteiro congele no meio do oceano ou da estrada.
* **Sinalização Hierárquica:** O `LedController` funciona corretamente como um *Andon* industrial. Mesmo que a inclinação esteja normal (`OK`), um impacto violento na aceleração sobrepõe a visualização geral para `CRITICAL` (Vermelho), alertando que a caixa foi comprometida.

---

## 6️⃣ Comentários Adicionais (Reflexões e Expansões)

* **Limitações do Arquétipo:** O modelo atual indica perigo em tempo real visualmente. No entanto, se o contêiner cair durante a noite no meio de uma viagem, ao estabilizar, o sistema voltará para `OK`, perdendo o histórico da infração caso ninguém o veja na hora.
* **Melhorias Futuras para IoT Logística:** A principal melhoria seria adicionar o registro de dados (Datalogging). Uma vez detectado um nível `CRITICAL`, o sistema gravaria a ocorrência em um Cartão SD ou a transmitiria via rádio (LoRa/GSM) criando uma "caixa preta" irrefutável para fins de acionamento de seguro de cargas.
* **Uso de Interrupções:** Para maximizar a vida útil da bateria, o Polling poderia ser substituído por *Wake-on-Motion* (IRQ). O processador ficaria adormecido durante toda a viagem e só "acordaria" para acender a luz vermelha no instante exato em que o MPU6050 acusasse um impacto fora do comum.
