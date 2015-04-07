(function () {
    'use strict';

    angular
        .module('fd.services.order', [])
        .factory('orderSrv', orderSrv);

    orderSrv.$inject = [
        '$http', '$q'
    ];

    function orderSrv($http, $q){
        return {
            get_current_menu: get_current_menu,
            send_order: send_order,
            get_order: get_order,
            save_order: save_order
        };

        function get_current_menu(){
            var url = base_url + '/menu/current';
            return $http.get(url);
        }

        function send_order(){
            var url = base_url + 'menu/order';
            return $http.get(url);
        }

        function save_order(order){
            localStorage.setItem('order', JSON.stringify(order));
        }

        function get_order(){
            return JSON.parse(localStorage.getItem('order'));
        }
    }
})();