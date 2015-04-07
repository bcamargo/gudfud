var app = angular.module('foodie', ['ui.router', 'fd.login', 'fd.registration', 'fd.order', 'ngMaterial']);

app.config(function ($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise('/login');

    $stateProvider.
        state('login', {
            url: '/login',
            templateUrl: 'modules/login/html/login.html',
            controller: 'LoginCtrl'
        }).
        state('registration-profile', {
            url: '/registro/perfil',
            templateUrl: 'modules/registration/html/registration-profile.html',
            controller: 'RegistrationProfileCtrl'
        }).
        state('order-menu', {
            url: '/pedido/menu',
            templateUrl: 'modules/order/html/menu.html',
            controller: 'MenuCtrl'
        }).
        state('order-confirmation', {
            url: '/pedido/confirmar',
            templateUrl: 'modules/order/html/order-confirmation.html',
            controller: 'OrderConfirmationCtrl'
        });
});

app.factory('AuthInterceptor', ['$q', '$window', function ($q, $window) {
    return {
        request: function (config) {
            var token;
            if (localStorage.getItem('auth_token')) {
                token = localStorage.getItem('auth_token');
            }
            if (token) {
                config.headers.Authorization = 'Token ' + token;
            }
            return config;
        },
        responseError: function (response) {
            //Only check if Unauthorized http code
            if (response.status === 401) {
                localStorage.removeItem('auth_token');
                $window.location.href = '/app/#/login';
            }
            return $q.reject(response);
        }
    };
}]);

app.config(['$httpProvider', function ($httpProvider) {
    $httpProvider.interceptors.push('AuthInterceptor');
}]);

app.config(function($mdThemingProvider){
    $mdThemingProvider.theme('default')
        .primaryPalette('deep-orange');

});


var base_url = 'http://localhost:8000/api';