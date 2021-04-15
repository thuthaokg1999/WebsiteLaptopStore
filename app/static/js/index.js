$(document).ready(function() {

    $('.carousel').carousel({
      interval: 2500
    });

    $('.post-lap').slick({
      slidesToShow: 4,
      slidesToScroll: 2,
      autoplay: true    ,
      autoplaySpeed: 2500,
      nextArrow: $('.next-lap'),
      prevArrow: $('.prev-lap'),
    });


    $('.post-acc').slick({
      slidesToShow: 4,
      slidesToScroll: 1,
      autoplay: true,
      autoplaySpeed: 3000,
      nextArrow: $('.next-acc'),
      prevArrow: $('.prev-acc'),
    });

});

