(function () {
    'use strict';

    angular
        .module('fd.order')
        .controller('MenuCtrl', MenuCtrl);

    MenuCtrl.$inject = [
        '$scope', '$state', 'userSrv', 'orderSrv'
    ];

    function MenuCtrl($scope, $state, userSrv, orderSrv) {
        $scope.menu = {};
        $scope.order = {
            'delivery_time': 12
        };
        $scope.confirm_order = confirm_order;
        $scope.select_menu_item = select_menu_item;
        $scope.selected_tab = 1;

        initialize();

        function initialize() {
            get_current_menu();
            get_profile();
        }

        function get_profile(){
            userSrv.get_profile()
                .success(function(data){
                    $scope.profile = data;
                });
        }

        function get_current_menu(){
            orderSrv.get_current_menu()
                .success(function(data){
                    $scope.menu.appetizer = [];
                    $scope.menu.main = [];
                    $scope.menu.beverage = [];
                    $scope.menu.dessert = [];
                    $scope.menu.datetime = data.datetime;

                    for(var index in data.menu_items){
                        var item = data.menu_items[index];
                        $scope.menu[item.type.toLowerCase()].push(item);
                    }
                });
        }

        function select_menu_item(menu_item){
            $scope.order[menu_item.type.toLowerCase()] = menu_item;
            if($scope.selected_tab < 5){
                $scope.selected_tab++;
            }
        }

        function confirm_order(){
            orderSrv.save_order($scope.order);
            $state.go('order-confirmation');

//            orderSrv.order_menu($scope.selected_items)
//                .success(function(data){
//                    console.log(data);
//                });
        }
    }
})();