pipeline {
         agent any
         stages {
                 stage('Install Dependencies from Package chromepass') {
                     steps {
                         echo 'Install Dependencies from Package chromepass'
                         sh 'pip3 install -r requirements.txt'
                     }
                 }
                 stage('Static Code Metrics') {

                    steps {
                        echo 'Style checks with pylint'
                        sh 'pylint --reports=y chromepass/ || exit 0'
                    }

                 }
                 stage('Build Distribution Packages') {
                    when {
                         expression {
                             currentBuild.result == null || currentBuild.result == 'SUCCESS'
                         }
                    }
                    steps {
                        echo 'Build Source Distribution'
                        sh 'python3 setup.py sdist'

                        echo 'Build Wheel Distribution'
                        sh 'python3 setup.py bdist_wheel'

                        echo 'Build chromepass binary'
                        sh 'pyinstaller --onefile --name chromepass chromepass/main.py'
                    }
                    post {
                        always {
                              archiveArtifacts (allowEmptyArchive: true,
                              artifacts: 'dist/*whl, dist/*.tar.gz, dist/chromepass', fingerprint: true)
                        }
                    }
                 }
                stage('Deploy to PyPI') {
                    when {
                        expression { "${env.GIT_BRANCH}" =~ "origin/release/" }
                        }
                    steps {
                        echo 'Deploy to PyPI'
                        sh "python3 -m twine upload dist/*"
                    }
                }
    }
}
