var app=angular.module('docketly-app', []);

var UI_URL = "http:///localhost:4000/fidelity";


app.controller('DocketlyHomeController', ['$scope','$http',function($scope, $http){
    $scope.extractData=function(){
        $scope.isUploading = true;
        var formData = new FormData(document.querySelector('#upload-form'));
        var uploadUrl = UI_URL;
        $http.post(uploadUrl, formData,{
            transformRequest: angular.identity,
            headers: {'Content-Type': undefined, 'Accept': 'application/json'}
        }).then(
            function successCallback(response) {
                $scope.isUploading = false;
                console.log("----11----")
                console.log(response.data.data)
                console.log("----2----")
                $scope.court_info = response.data.data;
                PDFObject.embed(response.data.data['pdf_file_path'], "#pdf-container");
            }, 
            function errorCallback(response) {
                $scope.isUploading = false;
                console.log('response');
            });
    };
}]);






