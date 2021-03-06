angular.module("app").controller("loginCtrl", function ($scope, loginService, userService, $state, $mdToast) {

    $scope.user = {};
    
    verificarLogin = function() {
        token = userService.getToken();
        
        if(token != null  && userService.getUser() != null) {
            $state.go("home");
        }
    };

    $scope.fazerLogin = function (user) {
        loginService.fazerLogin(user).then(
            function (data) {
                userService.storeToken(data["data"]);
                
                userService.requestUser(data["data"]).then(function (user, status) {
                    userService.storeUser(user["data"]);
                    $state.go("home");
                });
            },
            function(data) {
                user.senha = ""
                $mdToast.show(
                        $mdToast.simple()
                        .textContent("Combinação de login e senha incorreta.")
                        .highlightClass('md-warn')
                        .position('top left')
                        .action('OK')
                        .hideDelay(6000)
                    );
            }
            );
    };
    
    verificarLogin();

});