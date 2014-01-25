var scenterServices = angular.module('scenterServices', ['ngResource']);
 
scenterServices.factory('Fences', ['$resource',
  function($resource){
    return $resource('api/fences/', {}, {
      query: {method:'GET', params:{bbox:''}, isArray:true}
    });
  }]);