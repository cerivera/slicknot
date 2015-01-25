var SlicknotApp = angular.module('SlicknotApp', ['ui.bootstrap', 'ui.router']);



SlicknotApp.config(function($stateProvider, $urlRouterProvider) {
  $urlRouterProvider.otherwise("/");

  $stateProvider
      .state('root', {
          abstract: true,
          controller: function($scope) {

          },
          templateUrl : "partials/root.partial"
      })
      .state('root.index', {
          url: '/',
          templateUrl: 'parials/index.partial',
          controller: function($scope) {

          }
      });
});