(function () {
    'use strict';

    angular
        .module('fd.login')
        .controller('LoginCtrl', LoginCtrl);

    LoginCtrl.$inject = [
        '$scope', '$state', 'userSrv'
    ];

    function LoginCtrl($scope, $state, userSrv) {
        $scope.login = login;


        initialize();

        function initialize(){
            // oauth.io initilization
            OAuth.initialize('Xj4ohspQonfU5vQq9PnG8Caypkk');
        }

        function login(backend) {

            OAuth.popup(backend, function(error, success) {
                if (error) {
                    console.log('error', error);
                }
                else {
                    var token = success.access_token || success.oauth_token;

                    var data = {'token': token, 'backend': backend};
                    var loginPromise = userSrv.register(data);

                    loginPromise.success(function () {
                        $state.go('registration-profile');
                    });
                }
            });
        }
    }
})();

