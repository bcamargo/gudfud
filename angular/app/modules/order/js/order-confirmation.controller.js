(function () {
    'use strict';

    angular
        .module('fd.order')
        .controller('OrderConfirmationCtrl', OrderConfirmationCtrl);

    OrderConfirmationCtrl.$inject = [
        '$scope', '$state', 'userSrv', 'orderSrv'
    ];

    function OrderConfirmationCtrl($scope, $state, userSrv, orderSrv) {
        $scope.order = {};

        initialize();

        function initialize(){
            get_order();
        }

        function get_order(){
            $scope.order = orderSrv.get_order();
            $scope.delivery_time_range = get_delivery_time_range();
        }

        function get_delivery_time_range(){
            var delivery_time_range = {};
            var delivery_time = $scope.order.delivery_time;

            if(delivery_time == 12){
                delivery_time_range = {
                    'start': '12:00pm',
                    'end': '1:00pm'
                };
            }
            else if(delivery_time == 13){
                delivery_time_range = {
                    'start': '1:00pm',
                    'end': '2:00pm'
                };
            }
            else if(delivery_time == 14){
                delivery_time_range = {
                    'start': '2:00pm',
                    'end': '3:00pm'
                };
            }
            return delivery_time_range;
        }
    }
})();