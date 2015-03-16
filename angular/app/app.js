var app = angular.module('foodie', ['ui.router', 'uk.login']);
app.config(function ($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise('/login');

    $stateProvider.
        state('login', {
            url: '/login',
            templateUrl: 'modules/login/html/login.html',
            controller: 'LoginCtrl'
        });
});