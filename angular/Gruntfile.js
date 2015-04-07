'use strict';
module.exports = function (grunt) {

// Project configuration.

    grunt.initConfig({
        connect: {
            server: {
                options: {
                    port: 9001,
                    hostname: '0.0.0.0',
                    directory: 'app',
                    livereload: 35729
                }
            }
        },

        jshint: {
            all:{
                options: {
                    '-W024': true //ignore error when using delete (reserved word)
                },
                src: [
                    'app/**/*.js'
                ]
            }
        },

        concat: {
            dist: {
                files: {
                    'app/build/app.js': 'app/**/*.js'
                }
            }
        },

        uglify: {
            dist: {
                files: {
                    'app/build/app.js': [
                        'app/build/app.js'
                    ]
                }
            }
        },

        watch: {
            options: {
                livereload: true
            },
            js: {
                files: 'app/**/*.js',
                tasks: ['jshint']
            },
            html: {
                files: 'app/**/*.html'
            }
        },
        sass: {                              // Task
            dist: {                            // Target
                options: {                       // Target options
                    loadPath: ['bowe_components/foundation-apps/scss']
                }
            }
        }

    });

    grunt.loadNpmTasks('grunt-contrib-sass');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-connect');

    grunt.registerTask('default', []);
    grunt.registerTask('build', ['jshint', 'concat', 'uglify']);
    grunt.registerTask('serve', 'Compile then start a connect web server', function (target) {
        if (target === 'dist') {
          return grunt.task.run(['build', 'connect:dist:keepalive']);
        }

        grunt.task.run([
          'connect:server',
          'watch'
        ]);
    });
};
