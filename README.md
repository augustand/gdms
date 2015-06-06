# gdms
## graduation design manage system
##毕业设计管理系统


###创建虚拟环境
* 克隆仓库 git clone git@github.com:kooksee/gdms.git
* 创建虚拟环境 virtualenv venv --python=python2.7
* 创建activate的软链接，方便操作 ln -s activate venv/bin/activate
* 激活环境 source activate

###安装依赖包
* pip freeze > requirements && cat requirements
* pip install -r requirements
* sudo apt-get install postgresql libpq-dev python-dev
