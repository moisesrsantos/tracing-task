# Motor Practice Platform - Tracing Task

[![Build Status](https://travis-ci.org/moisesrsantos/tracing-task.svg?branch=master)](https://travis-ci.org/moisesrsantos/tracing-task)


Tracing Task é uma plataforma para executar o treinamento motor de tarefa de traçado de forma automática. Esta plataforma for desenvolvida para experimentos relacionados à aprendizagem de habilidade motora.

Tracing Task is a platform to automatic motor training of tracing task. This platform was designed to experiments about motor skill learning.


![Image of Tracing Task Experiment](https://github.com/moisesrsantos/tracing-task/blob/master/image/tracing-task-trial.jpg)


## Installation

Use the Anaconda [conda](https://www.anaconda.com/distribution/) to install.

```bash
git clone https://github.com/moisesrsantos/tracing-task.git
conda create -n tracing-task-env python=3.5
conda activate tracing-task-env
conda install -c anaconda tk
python -m pip install pygame
conda install -c menpo opencv
conda install -c anaconda pillow
```

## Usage

For use platform run this code:

```bash
conda activate tracing-task-env
python main.py
```

## Team

[Mateus Carvalho](http://lattes.cnpq.br/2756606178387194)

[Moisés Santos](https://github.com/moisesrsantos)

[Eduardo Souza](http://lattes.cnpq.br/9117085622535569)

[Lucas Silva](http://lattes.cnpq.br/6705692071878970)

[Paulo Almeida](http://lattes.cnpq.br/0035213619257246) (Project Coordinator)


## Cite Us

To cite Tracing Task platform in publications use:

- Santos, M. R., Souza, E. D., Carvalho, M. B., Oliveira, A. C., de Almeida Neto, A., Curado, M. R., & Ribeiro, P. R. (2019, July). Machine learning to estimate the amount of training to learn a motor skill. In International Conference on Human-Computer Interaction (pp. 198-209). Springer, Cham.
