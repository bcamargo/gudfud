(function () {
    'use strict';

    angular
        .module('fd.registration')
        .controller('RegistrationProfileCtrl', RegistrationProfileCtrl);

    RegistrationProfileCtrl.$inject = [
        '$scope', 'userSrv', '$state'
    ];

    function RegistrationProfileCtrl($scope, userSrv, $state) {
        $scope.save_profile = save_profile;
        $scope.profile = {};

        initialize();
        function initialize(){
            get_profile();
        }

        function get_profile(){
            userSrv.get_profile()
                .success(function(data){
                    $scope.profile = data;
                });
        }

        function save_profile() {
            console.log('save');
            userSrv.save_profile($scope.profile)
                .success(function(data){
                    $state.go('order-menu');
                });
        }
    }
})();