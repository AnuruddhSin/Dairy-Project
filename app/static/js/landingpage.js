function toggleMenu() {
    const menu = document.querySelector('.mobile-menu');
    menu.classList.toggle('active');
}

//  this is for homefooter to page1
document.addEventListener("DOMContentLoaded", function() {
const footerHome = document.querySelector(".homefooter");

footerHome.addEventListener("click", function() {
const page1 = document.getElementById("page1");
page1.scrollIntoView({ behavior: "smooth" }); // Smooth scroll to #page1
});
});


//  this is for homefooter to page1
document.addEventListener("DOMContentLoaded", function() {
    const footerHome = document.querySelector(".desktop_service");
    
    footerHome.addEventListener("click", function() {
    const page1 = document.getElementById("provide");
    page1.scrollIntoView({ behavior: "smooth" }); // Smooth scroll to #page1
    });
    });



gsap.from(".navbar",{
    y:30,
    opacity:1,
    duration:1,
    delay:1
})
gsap.from(".text1",{
    y:200,
    color:"black",
    opacity:0,
    duration:2,
    delay:1,
})


gsap.from(".text2",{
    x: 400,
    duration: 1,
    stagger: 1,
    delay: 1,
     opacity: 0,
 
    yoyo:true
    
})

gsap.from(".keyfeature_imgbox_container",{
    y:200,
    opacity:0,
    duration:0.1,

    
   

    scrollTrigger:".keyfeature_imgbox_container",
    
    })


// var nav = gsap.timeline()
   
// nav.from(".nav-item",{
//     y:-30,
//     opacity:0,
//     duration:1.2,
//     delay:0.5,
//     stagger:0.3
// })
// nav.from(".login",{
//     x:30,
//     opacity:0,
//     duration:1.2,
    
   
// })
// nav.from(".register",{
//     y:-30,
//     opacity:0,
//     duration:1.2,
    
   
// })

// nav.from(".knowmorebutton ",{
//     color:"black",
//     boderRadius:"100%",
//     x:100,
//     duration:2,
    
    
// })