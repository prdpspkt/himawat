/**
 * TinyMCE initialization
 * Configures TinyMCE to load from local static files
 */

document.addEventListener('DOMContentLoaded', function() {
    // Find all textareas with tinymce class or within tinymce-wrapper
    const textareas = document.querySelectorAll('textarea[name="content"], textarea[name="answer"], textarea[name="description"]');

    textareas.forEach(function(textarea) {
        // Skip if already initialized
        if (textarea.hasAttribute('data-mce-initialized')) {
            return;
        }

        // Get current value
        const initialValue = textarea.value;

        tinymce.init({
            selector: '#' + textarea.id,
            license_key: 'gpl',
            promotion: false,
            width: '100%',
            height: 500,
            min_height: 300,
            resize: true,

            // Load from local static files
            base_url: '/static/tinymce',
            suffix: '.min',

            // Theme and skin
            skin: 'oxide',
            theme: 'silver',
            content_css: '/static/tinymce/skins/content/default/content.css',

            // Plugins - using community edition plugins
            plugins: [
                'advlist', 'autolink', 'lists', 'link', 'image', 'charmap', 'preview',
                'anchor', 'searchreplace', 'visualblocks', 'code', 'fullscreen',
                'insertdatetime', 'media', 'table', 'help', 'wordcount'
            ],

            // Toolbar configuration
            toolbar: 'undo redo | blocks | bold italic underline strikethrough | ' +
                     'alignleft aligncenter alignright alignjustify | ' +
                     'bullist numlist outdent indent | forecolor backcolor | ' +
                     'link image media table | code preview fullscreen | help',

            // Menu bar
            menubar: 'file edit view insert format tools table help',

            // Menu configuration
            menu: {
                file: { title: 'File', items: 'newdocument restoredraft | preview | print ' },
                edit: { title: 'Edit', items: 'undo redo | cut copy paste pastetext | selectall | searchreplace' },
                view: { title: 'View', items: 'code visualblocks' },
                insert: { title: 'Insert', items: 'image link media addinserttable template codesample insertdatetime | charmap emoticons hr | pagebreak nonbreaking anchor toc | insertdatetime' },
                format: { title: 'Format', items: 'bold italic underline strikethrough superscript subscript codeformat | styles blocks fontfamily fontsize align lineheight | forecolor backcolor | removeformat' },
                tools: { title: 'Tools', items: 'spellchecker spellcheckerlanguage | code wordcount' },
                table: { title: 'Table', items: 'inserttable | cell row column | advtablesort | tableprops deletetable' },
                help: { title: 'Help', items: 'help' }
            },

            // Block formats
            block_formats: 'Paragraph=p; Heading 1=h1; Heading 2=h2; Heading 3=h3; Heading 4=h4; Heading 5=h5; Heading 6=h6; Preformatted=pre',

            // Font sizes
            fontsize_formats: '8pt 10pt 12pt 14pt 16pt 18pt 20pt 24pt 28pt 32pt 36pt 48pt 72pt',

            // Image upload configuration
            images_upload_url: '/api/media/upload/',
            images_upload_credentials: true,
            images_upload_handler: function (blobInfo, success, failure) {
                const xhr = new XMLHttpRequest();
                xhr.withCredentials = true;

                xhr.open('POST', '/api/media/upload/');
                xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));

                xhr.onload = function() {
                    if (xhr.status === 200) {
                        const json = JSON.parse(xhr.responseText);
                        success(json.location);
                    } else {
                        failure('Image upload failed: ' + xhr.statusText);
                    }
                };

                const formData = new FormData();
                formData.append('file', blobInfo.blob(), blobInfo.filename());

                xhr.send(formData);
            },

            // Link settings
            link_default_target: '_blank',
            link_title: false,

            // Content styling
            content_style: 'body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, sans-serif; font-size: 14px; }',

            // Allow all HTML elements and attributes
            valid_elements: '*[*]',

            // Allow all style attributes
            valid_styles: {
                '*': 'color,font-size,font-family,background-color,font-weight,font-style,text-decoration,float,margin,margin-top,margin-right,margin-bottom,margin-left,padding,padding-top,padding-right,padding-bottom,padding-left,display,text-align,vertical-align,border,border-width,border-style,border-color,list-style-type,list-style-position,position,top,left,right,bottom,width,height,overflow,text-transform,line-height,letter-spacing,word-spacing,white-space,background,background-image,background-repeat,background-position,background-size'
            },

            // Initialize with content
            setup: function(editor) {
                // Set initial content
                if (initialValue) {
                    editor.setContent(initialValue);
                }

                // Mark textarea as initialized
                textarea.setAttribute('data-mce-initialized', 'true');

                // Update textarea on change
                editor.on('change keyup', function() {
                    textarea.value = editor.getContent();
                });

                // Handle form submission
                const form = textarea.closest('form');
                if (form) {
                    form.addEventListener('submit', function() {
                        textarea.value = editor.getContent();
                    });
                }
            }
        });
    });

    // Helper function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
