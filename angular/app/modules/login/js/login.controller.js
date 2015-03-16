(function () {
    'use strict';

    angular
        .module('uk.login')
        .controller('LoginCtrl', LoginCtrl);

    LoginCtrl.$inject = [
        '$scope', '$http'
    ];

    function LoginCtrl($scope, $http) {
        $scope.loginBK = function (backend) {

            OAuth.popup(backend, function(error, success) {
                if (error) {

                }
                else {
                    var token = success.access_token || success.oauth_token;
                    var url = 'http://0.0.0.0:8000/api/users/access-token';
                    var data = {'token': token, 'backend': backend};
                    var loginPromise = $http.post(url, data);

                    $scope.login.working = true;

                    loginPromise.success(function () {
                      $scope.login = { working: false };
                    });

                    loginPromise.finally(function () {
                      $scope.login.working = false;
                    });

                }
            });
        };

        // oauth.io initilization
        OAuth.initialize('Xj4ohspQonfU5vQq9PnG8Caypkk');
    }
})();

