let mainImg = $("#diaryimg")

function change(number) {
    mainImg.attr("src", `/static/css/User/image/diary${number}.jpg`)
    mainImg.attr("alt", "/static/css/User/image/diary1.jpg")
}

function getRandom() {
    let img_count = 7
    let num = Math.floor(Math.random() * img_count) + 1;

    change(num)
}

getRandom()