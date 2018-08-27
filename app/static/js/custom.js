// function setSession(){
//     var sess = $('#sess').val();
//
//     if (sessionStorage.getItem('admin')) {
//
//     }else if(!sess){
//         window.location.href ='/#loginFirst';
//     }else {
//         sessionStorage.setItem('session',sess)
//     }
//
//
// }
//
// function checkSession(){
//     if (sessionStorage.getItem('admin')){
//         window.location.href ='/dashboard';
//     }
//
// }

$(document).ready(function () {


        $( "#myForm" ).on( "submit", function( event ) {
          event.preventDefault();
          var str = $(this).serialize();

          $.ajax({
                method: "POST",
                url: '/addbook',
                data: str,
                dataType: 'JSON',
                success: function (data) {
                    console.log(data)
                    if (data === 200) {
                        window.location.href ='/bookaddsuccess';                    }
                },
            });
        });

        $( "#myForm2" ).on( "submit", function( event ) {
          event.preventDefault();
          var str = $(this).serialize();

          $.ajax({
                method: "POST",
                url: '/addgenre',
                data: str,
                dataType: 'JSON',
                success: function (data) {
                    console.log(data)
                    if (data === 200) {
                        window.location.href ='/genreaddsuccess';                    }
                },
            });
        });

        if (location.hash === '#success') {
            $.notify({
                icon: '<i class="material-icons">grade</i>',
                message: "Success!"
            }, {
                type: 'success',
                animate: {
                    enter: 'animated fadeInUp',
                    exit: 'animated fadeOutRight'
                },
                placement: {
                    from: "top",
                    align: "center"
                },
                offset: 10,
                spacing: 10,
                z_index: 1031,
            });
            window.location.replace(location.href.split('#')[0] + '#');
        }

        if (location.hash === '#loginFirst') {
            $.notify({
                icon: '<i class="material-icons">grade</i>',
                message: "Login First!"
            }, {
                type: 'success',
                animate: {
                    enter: 'animated fadeInUp',
                    exit: 'animated fadeOutRight'
                },
                placement: {
                    from: "top",
                    align: "center"
                },
                offset: 10,
                spacing: 10,
                z_index: 1031,
            });
            window.location.replace(location.href.split('#')[0] + '#');
        }

        if (location.hash === '#bookdelete') {
            $.notify({
                icon: '<i class="material-icons">grade</i>',
                message: "Book Deleted Successfully!"
            }, {
                type: 'success',
                animate: {
                    enter: 'animated fadeInUp',
                    exit: 'animated fadeOutRight'
                },
                placement: {
                    from: "top",
                    align: "center"
                },
                offset: 10,
                spacing: 10,
                z_index: 1031,
            });
            window.location.replace(location.href.split('#')[0] + '#');
        }
        if (location.hash === '#bookadd') {
            $.notify({
                icon: '<i class="material-icons">grade</i>',
                message: "Book Added Successfully!"
            }, {
                type: 'success',
                animate: {
                    enter: 'animated fadeInUp',
                    exit: 'animated fadeOutRight'
                },
                placement: {
                    from: "top",
                    align: "center"
                },
                offset: 10,
                spacing: 10,
                z_index: 1031,
            });
            window.location.replace(location.href.split('#')[0] + '#');
        }

        if (location.hash === '#genreadd') {
            $.notify({
                icon: '<i class="material-icons">grade</i>',
                message: "Genre Added Successfully!"
            }, {
                type: 'success',
                animate: {
                    enter: 'animated fadeInUp',
                    exit: 'animated fadeOutRight'
                },
                placement: {
                    from: "top",
                    align: "center"
                },
                offset: 10,
                spacing: 10,
                z_index: 1031,
            });
            window.location.replace(location.href.split('#')[0] + '#');
        }

        if (location.hash === '#genredelete') {
            $.notify({
                icon: '<i class="material-icons">grade</i>',
                message: "Genre Deleted Successfully!"
            }, {
                type: 'success',
                animate: {
                    enter: 'animated fadeInUp',
                    exit: 'animated fadeOutRight'
                },
                placement: {
                    from: "top",
                    align: "center"
                },
                offset: 10,
                spacing: 10,
                z_index: 1031,
            });
            window.location.replace(location.href.split('#')[0] + '#');
        }

        if (location.hash === '#userdelete') {
            $.notify({
                icon: '<i class="material-icons">grade</i>',
                message: "User Deleted Successfully!"
            }, {
                type: 'success',
                animate: {
                    enter: 'animated fadeInUp',
                    exit: 'animated fadeOutRight'
                },
                placement: {
                    from: "top",
                    align: "center"
                },
                offset: 10,
                spacing: 10,
                z_index: 1031,
            });
            window.location.replace(location.href.split('#')[0] + '#');
        }
        if (location.hash === '#failed') {
            $.notify({
                icon: 'glyphicon glyphicon-star',
                message: "Failed to add data!,Contact Administrator"
            }, {
                type: 'danger',
                animate: {
                    enter: 'animated fadeInUp',
                    exit: 'animated fadeOutRight'
                },
                placement: {
                    from: "top",
                    align: "center"
                },
                offset: 10,
                spacing: 10,
                z_index: 1031,
            });
            window.location.replace(location.href.split('#')[0] + '#');
        }
        if (location.hash === '#loginFailed') {
            $.notify({
                icon: '',
                message: "Wrong Credentials"
            }, {
                type: 'danger',
                animate: {
                    enter: 'animated fadeInUp',
                    exit: 'animated fadeOutRight'
                },
                placement: {
                    from: "top",
                    align: "center"
                },
                offset: 10,
                spacing: 10,
                z_index: 1031,
            });
            window.location.replace(location.href.split('#')[0] + '#');
        }
    })

