const CANVAS_SIZE = 320;


function load_uploaded_image(url) {
    clear_all_canvas()
    var c = document.getElementById("loaded_image");
    var cxt = c.getContext("2d");
    var img = new Image();
    img.src = url;
    img.onload = function () {
        const size2 = 320;
        if (img.width >= img.height) {
            var new_width = CANVAS_SIZE;
            var new_height = img.height / img.width * new_width
        } else {
            var new_height = CANVAS_SIZE;
            var new_width = img.width / img.height * new_height
        }
        cxt.drawImage(img, 0, 0, new_width, new_height);
    }
}

function load_mask(url) {
    var c = document.getElementById("mask");
    var cxt = c.getContext("2d");
    var img = new Image();
    img.src = url;
    img.onload = function () {
        const size2 = 320;
        if (img.width >= img.height) {
            var new_width = 320;
            var new_height = img.height / img.width * new_width
        } else {
            var new_height = 320;
            var new_width = img.width / img.height * new_height
        }
        cxt.drawImage(img, 0, 0, new_width, new_height);
    }
}

function load_object(url) {
    var c = document.getElementById("object");
    var cxt = c.getContext("2d");
    var img = new Image();
    img.src = url;
    img.onload = function () {
        const size2 = 320;
        if (img.width >= img.height) {
            var new_width = 320;
            var new_height = img.height / img.width * new_width
        } else {
            var new_height = 320;
            var new_width = img.width / img.height * new_height
        }
        cxt.drawImage(img, 0, 0, new_width, new_height);
    }
}

function show_uploaded() {
    var form = new FormData(document.getElementById("upload_form"));
    $.ajax({
        url: "{{ url_for('load_uploaded_image') }}",
        type: "post",
        data: form,
        dataType: 'json',
        processData: false,
        contentType: false,
        success: function (data) {
            alert(data.image_url)
        },
        error: function (e) {
            alert("error");
        }
    })
}

$("#choose_image").change(function () {
    var fileObj = document.getElementById("choose_image").files[0]; // js 获取文件对象
    var formFile = new FormData();
    formFile.append("action", "UploadVMKImagePath");
    formFile.append("file", fileObj); //加入文件对象

    var data = formFile;
    $.ajax({
        url: "/load_uploaded_image",
        data: data,
        type: "Post",
        dataType: "json",
        cache: false,//上传文件无需缓存
        processData: false,//用于对data参数进行序列化处理 这里必须false
        contentType: false, //必须
        success: function (data) {
            url = data["image_url"]
            load_uploaded_image(url)
        },
    })
})

$("#infer").click(function () {
    var name = document.getElementById("choose_image").files[0].name
    $.ajax({
        url: "/infer",
        data: {
            "image_name": name
        },
        type: "Post",
        dataType: "json",
        success: function (data) {
            load_object(data["object_url"])
            load_mask(data["mask_url"])
        },
    })
})

function clear_all_canvas() {
    var c1=document.getElementById("loaded_image");
    var cxt=c1.getContext("2d");
    c1.height=c1.height;

    var c2=document.getElementById("mask");
    var cxt=c2.getContext("2d");
    c2.height=c2.height;

    var c3=document.getElementById("object");
    var cxt=c3.getContext("2d");
    c3.height=c3.height;
}

