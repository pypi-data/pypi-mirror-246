function LabXBlock(runtime, element) {

    const translations = {
        'Upload a Zip file': {
          'en': 'Upload a Zip file.',
          'vi': 'Tải file Zip lên',
        },
        "Compress your project files into a single uncompressed Zip file on your computer limited to 500 MB." :{
            "en" : "Compress your project files into a single uncompressed Zip file on your computer limited to 500 MB.",
            "vi": "Nén (các) tệp dự án của bạn thành mọt tệp zip duy nhất trên máy tính của bạn, giới hạn 500 MB (không nén)"
        },
        "Select file" : {
            "en" : "Select file" ,
            "vi" : "Chọn file"
        },
        "Submission date" : {
            "en" : "Submission date",
            "vi" : "Ngày nộp"
        },
        "Lab content" : {
            "en" : "Lab content" ,
            "vi" : "Nội dung bài lab"
        },
        "Reference answers" : {
            "en" : "Reference answers",
            "vi" : "Đáp án tham khảo"
        },
        "View Lab reference answers" : {
            "en" : "View Lab reference answers",
            "vi" : "Xem đáp án tham khảo bài Lab"
        },
        "Download submitted lab" : {
            "en" : "Download submitted lab",
            "vi" : "Tải xuống bài đã nộp"
        }

      };

    function trans(word) {
        const cookieValue = $.cookie('openedx-language-preference');
    
        return  translations[word][cookieValue] ? translations[word][cookieValue] : translations[word]['en'] ;
    }

   
    const  usageId =element.getAttribute('data-usage-id')

    $.ajax({
        type: "GET",
        url: runtime.handlerUrl(element, 'lab'),
        success: function(data) {
               if (data.block_id == usageId){
                const labElement = $(element).find('#lab');
                if (data.type === 'text'){
                    if ( !data.result_student){
                        const btnLabText = $(element).find('#btn-lab-text');
                        const btnSubmit = $(element).find('#btn-lab-submit')
                        btnLabText.removeClass('none')
                        
                        $('#btn-lab-text', element).click(function (event){
                            btnSubmit.removeClass('none')
                            let newDiv = `
                            <div id='editor'></div>`
                            labElement.append(newDiv);
                             ClassicEditor
                            .create( element.querySelector( '#editor' ) ).then(editor =>{
                                btnLabText.addClass('none')
                                btnSubmit.click(function (event){
                                    const editorData = editor.getData();
                                    const formData = new FormData();
                                    formData.append("text", editorData);
                                    formData.append('type', 'lab');
                                    $.ajax({
                                        type: "POST",
                                        url: runtime.handlerUrl(element, 'lab_text'),
                                        contentType: false,
                                        processData: false,
                                        data: formData,
                                        success: (data)=>{
                                            viewResultText(data)
                                        }
                                    });
                                }).catch( error => {
                                            console.error( error );
                             } );
                            })})
                    }else {
                        viewResultText(data)
                       

                        
                    }
        
                }else if (data.type == 'file'){
                    $('.lab-text', element).remove()
                   
                    // console.log('data', data)
                    if (data.url.length == 0){
                        const inputHtml = ` 
                        <div class='notify-upload'>
                            <span>${trans('Upload a Zip file')}</span>
                            <span> ${trans('Compress your project files into a single uncompressed Zip file on your computer limited to 500 MB.')} </span>
                        </div>
                        <div>
                        <input type="file" name="file" id="file" class="inputfile"  />      
                        <label for="file">${trans('Select file')}</label>
                        </div>
                            <div id='file-info'></div>
                        `;
                        labElement.append(inputHtml);
                        $(element).on('change', '.inputfile', function() {
                            const selectedFile = this.files[0];
                            const fileInfoContainer = $('#file-info');
                            if (selectedFile) {
                                fileInfoContainer.html(`
                                   <div class='info-file-content'>
                                    <span><i class="fa fa-file-text" aria-hidden="true"></i> ${selectedFile.name}</span>
                                    <span><i class="fa fa-times" aria-hidden="true"></i></span>
                                   </div>
                                `);
                                $('.inputfile').css('display', 'none');
                                $('label[for="file"]').css('display', 'none');
                                $(element).find('#btn-lab-submit').removeClass('none')
                                $(element).find('.lab-btn').css('text-align' , 'start')

                                $('.fa-times' , element).click(function (){
                                    $('.error-message', element).remove()
                                    $('#file')[0].value = '';
                                    $('.info-file-content', element).remove()
    
                                    $('.inputfile').css('display', 'inline-block');
                                    $('label[for="file"]').css('display', 'inline-block');
                                    $(element).find('#btn-lab-submit').addClass('none')
                                })
                                $(element).find('#btn-lab-submit').click(function (){
                                    const selectedFile = $('#file')[0].files[0];
                                    if (selectedFile) {
                                        const fileSizeInMB = selectedFile.size / (1024 * 1024)
                                        const fileType = selectedFile.type;
                                        if (fileSizeInMB > 5) {
                                            $('.error-message', element).remove()
                                            $('#lab').append('<span class="error-message">File size exceeds 5MB limit</span>');
                                        }else if (fileType !== 'application/zip' ){
                                            $('.error-message', element).remove()
                                            $('#lab').append('<span class="error-message">File must be a ZIP file</span>');
                                        }
                                        else {
                                            const formData = new FormData();
                                            formData.append("file", selectedFile);
                                            formData.append('type', 'lab');
                                            $.ajax({
                                                type: "POST",
                                                url: runtime.handlerUrl(element, 'upload'),
                                                contentType: false,
                                                processData: false,
                                                data: formData,
                                                success: (data)=>{
                                                    $('.error-message', element).remove()
                                                    viewUpload(data)
                                                }
                                            });
                                           
                                        }
                                       
                                    } else {
                                        console.log('No file selected');
                                    }
                                })
    
                            } else {
                                fileInfoContainer.html('<p>Không có file được chọn.</p>');
    
                            }
                        });
                
                    }else {
                        viewUpload(data)
                    }


                }
             

               }   
        }
    });



    function viewDateSuccess(date){
        let dateObject = new Date(date);
        let year = dateObject.getFullYear();
        let month = dateObject.getMonth() + 1; 
        let day = dateObject.getDate();
        let formattedDate = day + '/' + month + '/' + year;
        let text = `${trans('Submission date')}: ${formattedDate}`
        $('.lab-date-success', element).html(text)
    }

    function viewResultText(data){
        viewDateSuccess(data.date)
        $('.lab-text', element).remove()

       const text = `
            <div>
                <div class='student-lab'>
                    <div class='student-lab-title'>
                        <span>${trans('Lab content')}</span>
                        <span  id='student-lab-edit'><i class="fa fa-pencil-square-o" aria-hidden="true"></i></span>
                    </div>
                    <div  class='student-lab-content'>
                        <span id='content-student-lab'> ${data.result_student}</span>
                    </div>
                </div>
                <div class='result-lab'>
                    <span class='result-lab-title'>${trans('Reference answers')}</span>
                    <div class='result-container'> 
                    <span> ${trans('View Lab reference answers')}</span>
                    <details class="detail-lab-result">
                        <summary class='result-summary'>
                            <span>${trans('Reference answers')}</span>
                            <span style='color:black'><i class="fa fa-chevron-right" aria-hidden="true"></i></span>
                        </summary>
                        <div >
                            <span style='padding-bottom:10px; padding-top:5px ; font-weight:500; font-size:16px'>${data.result}</span>
                        </div>
                    </details>
                        
                    </div>
                </div>
            </div>
        `
        $(".lab-content", element).html(text);
        $('#lab-notification').removeClass('none');
        $(element).find('.detail-lab-result').on('toggle', function() {
            var $iconSpan = $(element).find('.fa-chevron-right');
            if ($(this).prop('open')) {
                $iconSpan.hide(); 
            } else {
                $iconSpan.show(); 
            }
        });

        $("#student-lab-edit" , element).click(function(){
            $("#content-student-lab" , element).addClass('none')
            const labElement = $(element).find('.student-lab-content');
            let newDiv = `
            <div id='lab-edit'>
                <div id='editor'>
                    <span>${data.result_student}</span>
                </div>
                <div class='btn-edit'>  
                        
                        <div class="lab-btn ">
                            <span id='lab-huy'  class="lab-button" >
                                <span class="text-lab">Huỷ</span>
                            </span>
                        </div>
                        <div class="lab-btn ">
                            <span id='student-edit-submit'  class="lab-button" >
                                <span class="text-lab">Chỉnh sửa</span>
                            </span>
                        </div>
                 </div>
            </div>
            `
            labElement.append(newDiv);
             ClassicEditor
            .create( element.querySelector( '#editor' ) ).then(editor =>{
                $('#lab-huy', element).click(function(){
                    $("#content-student-lab" , element).removeClass('none')
                    $("#lab-edit" , element).remove()
                })
                $('#student-edit-submit' , element).click(function(){
                    const editorData = editor.getData();
                    const formData = new FormData();
                    formData.append("text", editorData);
                    formData.append('type', 'lab');
                    $.ajax({
                        type: "POST",
                        url: runtime.handlerUrl(element, 'lab_text'),
                        contentType: false,
                        processData: false,
                        data: formData,
                        success: (data)=>{
                            viewResultText(data)

                        }
                    });
                })
            })
        })
    }

    function viewUpload (data){

        $('.lab-text', element).remove()
        viewDateSuccess(data.date)
        $('.inputfile').css('display', 'none');
        $('label[for="file"]').css('display', 'none');
        $('.notify-upload').css('display', 'none');
        const text = `
        <div>
            <div class='student-lab'>
                <div >
                    <a class='student-file'  href=${data.url} target='_blank' > 
                        <span>${trans('Download submitted lab')} </span>
                    </a>
                </div>
            </div>
            <div class='result-lab'>
                <span class='result-lab-title' >${trans('Reference answers')}</span>
                <div class='result-container'> 
                <span> ${trans('View Lab reference answers')}</span>
                <details class="detail-lab-result">
                    <summary class='result-summary'>
                        <span>${trans('Reference answers')}</span>
                        <span style='color:black'><i class="fa fa-chevron-right" aria-hidden="true"></i></span>
                    </summary>
                    <div >
                        <span style='padding-bottom:10px; padding-top:5px'>${data.result}</span>
                    </div>
                </details>
                    
                </div>
            </div>
        </div>
    `
    $(".lab-content", element).html(text);
    $('#lab-notification').removeClass('none');
    }



}