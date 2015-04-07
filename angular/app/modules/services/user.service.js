(function () {
    'use strict';

    angular
        .module('fd.services.user', [])
        .factory('userSrv', userSrv);

    userSrv.$inject = [
        '$http', '$q'
    ];

    function userSrv($http, $q) {
        return {
            save_profile: save_profile,
            get_profile: get_profile,
            register: register
        };

        function register(data){
            var url = base_url + '/users/access-token';
            return $http.post(url, data)
                .success(function(data){
                    localStorage.setItem('auth_token', data.token);
                });
        }

        function get_profile(){
            var url = base_url + '/users/profile';
            return $http.get(url);
        }

        function save_profile(data){
            var url = base_url + '/users/profile';

            if ('image' in data) {
                delete data.image;
            }

            return $http.patch(url, data);
        }
    }

})();