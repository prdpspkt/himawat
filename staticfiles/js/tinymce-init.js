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
            content_css: [
                'https://cdn.jsdelivr.net/npm/tailwindcss@3.4.17/dist/tailwind.min.css',
                '/static/css/style.css'
            ],

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
                     'link image media table | code preview | aiassistant fullscreen | help',

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

            // Content styling - base styles to ensure immediate visual feedback
            content_style: 'body { font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, sans-serif; font-size: 16px; line-height: 1.8; color: #374151; }',

            // Fullscreen configuration
            fullscreen_native: true,
            toolbar_sticky: true,
            toolbar_mode: 'wrap',

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

                // Function to sync content to textarea
                const syncContent = function() {
                    textarea.value = editor.getContent();
                };

                // Update textarea on multiple events
                editor.on('change keyup blur', function() {
                    syncContent();
                });

                // Also sync periodically (every 2 seconds)
                setInterval(syncContent, 2000);

                // Handle form submission
                const form = textarea.closest('form');
                if (form) {
                    // Sync on form submit
                    form.addEventListener('submit', function(e) {
                        syncContent();
                    });

                    // Find all submit buttons in the form and sync on click
                    const submitButtons = form.querySelectorAll('button[type="submit"], input[type="submit"]');
                    submitButtons.forEach(function(btn) {
                        btn.addEventListener('click', function(e) {
                            syncContent();
                        });
                    });
                }

                // Add AI Assistant button
                editor.ui.registry.addButton('aiassistant', {
                    text: '✨ AI Assistant',
                    icon: 'browse',
                    tooltip: 'Generate or edit content with AI',
                    onAction: function() {
                        openAIPanel(editor);
                    }
                });
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

    // Open AI Assistant panel
    function openAIPanel(editor) {
        const currentContent = editor.getContent();

        // Create modal dialog
        const modal = document.createElement('div');
        modal.style.cssText = 'position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 10000; display: flex; align-items: center; justify-content: center;';

        modal.innerHTML = `
            <div style="background: white; border-radius: 12px; width: 90%; max-width: 600px; max-height: 85vh; overflow-y: auto; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);">
                <div style="padding: 24px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                        <h2 style="margin: 0; font-size: 20px; font-weight: 600; color: #1f2937;">✨ AI Assistant</h2>
                        <button id="close-modal" style="background: none; border: none; font-size: 24px; cursor: pointer; color: #6b7280;">&times;</button>
                    </div>

                    <div id="ai-setup-form">
                        <div style="margin-bottom: 20px;">
                            <label style="display: block; font-size: 14px; font-weight: 500; color: #374151; margin-bottom: 8px;">Action</label>
                            <select id="ai-action" style="width: 100%; padding: 10px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 14px;">
                                <option value="generate">Generate new content</option>
                                <option value="replace">Replace current content</option>
                                <option value="edit">Edit/improve current content</option>
                            </select>
                        </div>

                        <div style="margin-bottom: 20px;">
                            <label style="display: block; font-size: 14px; font-weight: 500; color: #374151; margin-bottom: 8px;">Prompt</label>
                            <textarea id="ai-prompt" rows="4" placeholder="Describe what you want to generate or how you want to edit the content..." style="width: 100%; padding: 10px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 14px; resize: vertical;"></textarea>
                        </div>

                        <div style="display: flex; gap: 10px; justify-content: flex-end;">
                            <button id="ai-cancel" style="padding: 10px 20px; border: 1px solid #d1d5db; background: white; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: 500;">Cancel</button>
                            <button id="ai-generate" style="padding: 10px 20px; background: #4f46e5; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: 500;">Generate</button>
                        </div>
                    </div>

                    <div id="ai-loading" style="display: none; margin-top: 16px; text-align: center; padding: 20px;">
                        <div style="display: inline-block; animation: spin 1s linear infinite; margin-right: 8px; font-size: 24px;">✨</div>
                        <div style="color: #6b7280; font-size: 14px; margin-top: 8px;">Generating content, please wait...</div>
                    </div>

                    <div id="ai-result" style="display: none;">
                        <div style="margin-bottom: 16px;">
                            <label style="display: block; font-size: 13px; font-weight: 500; color: #374151; margin-bottom: 8px;">Generated Content:</label>
                            <div id="ai-preview" style="padding: 12px; border: 1px solid #d1d5db; border-radius: 6px; background: #f9fafb; max-height: 300px; overflow-y: auto; font-size: 14px; line-height: 1.6; color: #374151;"></div>
                        </div>

                        <div style="display: flex; gap: 10px; justify-content: flex-end;">
                            <button id="ai-retry" style="padding: 8px 16px; border: 1px solid #d1d5db; background: white; border-radius: 6px; cursor: pointer; font-size: 13px; font-weight: 500;">Retry</button>
                            <button id="ai-insert" style="padding: 8px 16px; background: #10b981; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 13px; font-weight: 500;">Insert Content</button>
                            <button id="ai-close-result" style="padding: 8px 16px; border: 1px solid #d1d5db; background: white; border-radius: 6px; cursor: pointer; font-size: 13px; font-weight: 500;">Close</button>
                        </div>
                    </div>

                    <div id="ai-error" style="display: none; margin-top: 16px; padding: 12px; background: #fef2f2; border: 1px solid #fecaca; border-radius: 6px; color: #991b1b; font-size: 14px;"></div>
                </div>
            </div>
            <style>
                @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
                @keyframes pulse {
                    0%, 100% { opacity: 1; transform: scale(1); }
                    50% { opacity: 0.5; transform: scale(0.95); }
                }
            </style>
        `;

        document.body.appendChild(modal);

        const closeModal = () => document.body.removeChild(modal);
        modal.querySelector('#close-modal').onclick = closeModal;
        modal.querySelector('#ai-cancel').onclick = closeModal;
        modal.querySelector('#ai-close-result').onclick = closeModal;

        let generatedContent = '';
        let isStreamRunning = false;

        // Function to strip markdown code blocks from content
        const stripMarkdownCodeBlocks = (content) => {
            // Remove ```html or ``` code blocks
            const codeBlockRegex = /```(?:html|HTML)?\n([\s\S]*?)```/g;
            const match = content.match(codeBlockRegex);

            if (match) {
                // Extract content from code block
                let extracted = content.replace(codeBlockRegex, '$1');
                return extracted.trim();
            }

            // If no code block, return as-is
            return content;
        };

        // Function to check stream status
        const checkStreamStatus = () => ({
            isRunning: isStreamRunning,
            hasContent: generatedContent.length > 0,
            contentLength: generatedContent.length
        });

        // Function to update button states
        const updateButtonStates = (disabled) => {
            const retryBtn = modal.querySelector('#ai-retry');
            const insertBtn = modal.querySelector('#ai-insert');
            const closeBtn = modal.querySelector('#ai-close-result');

            if (retryBtn) retryBtn.disabled = disabled;
            if (insertBtn) insertBtn.disabled = disabled;
            if (closeBtn) closeBtn.disabled = disabled;

            // Update visual appearance
            if (disabled) {
                if (retryBtn) {
                    retryBtn.style.opacity = '0.5';
                    retryBtn.style.cursor = 'not-allowed';
                }
                if (insertBtn) {
                    insertBtn.style.opacity = '0.5';
                    insertBtn.style.cursor = 'not-allowed';
                }
                if (closeBtn) {
                    closeBtn.style.opacity = '0.5';
                    closeBtn.style.cursor = 'not-allowed';
                }
            } else {
                if (retryBtn) {
                    retryBtn.style.opacity = '1';
                    retryBtn.style.cursor = 'pointer';
                }
                if (insertBtn) {
                    insertBtn.style.opacity = '1';
                    insertBtn.style.cursor = 'pointer';
                }
                if (closeBtn) {
                    closeBtn.style.opacity = '1';
                    closeBtn.style.cursor = 'pointer';
                }
            }
        };

        // Initialize retry and insert buttons as disabled
        updateButtonStates(true);

        // Update stream status UI
        const updateStreamStatusUI = (running, finished = false) => {
            let statusDiv = modal.querySelector('#ai-stream-status');
            const resultDiv = modal.querySelector('#ai-result');
            if (!statusDiv) {
                statusDiv = document.createElement('div');
                statusDiv.id = 'ai-stream-status';
                statusDiv.style.cssText = 'padding: 8px 12px; border-radius: 6px; font-size: 13px; margin-bottom: 12px;';
                if (resultDiv) {
                    resultDiv.insertBefore(statusDiv, resultDiv.firstChild);
                }
            }

            if (running) {
                statusDiv.style.background = '#dbeafe';
                statusDiv.style.color = '#1e40af';
                statusDiv.innerHTML = `
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="animation: pulse 1.5s ease-in-out infinite;">🔄</span>
                        <span>Generating content... (${generatedContent.length} characters)</span>
                    </div>
                `;
            } else if (finished) {
                statusDiv.style.background = '#d1fae5';
                statusDiv.style.color = '#065f46';
                statusDiv.innerHTML = `
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span>✅</span>
                        <span>Generation completed! (${generatedContent.length} characters)</span>
                    </div>
                `;
            } else {
                statusDiv.remove();
            }
        };

        modal.querySelector('#ai-generate').onclick = async () => {
            const action = modal.querySelector('#ai-action').value;
            const prompt = modal.querySelector('#ai-prompt').value.trim();
            const setupForm = modal.querySelector('#ai-setup-form');
            const loadingDiv = modal.querySelector('#ai-loading');
            const resultDiv = modal.querySelector('#ai-result');
            const previewDiv = modal.querySelector('#ai-preview');
            const errorDiv = modal.querySelector('#ai-error');
            const generateBtn = modal.querySelector('#ai-generate');

            if (!prompt) {
                errorDiv.textContent = 'Please enter a prompt.';
                errorDiv.style.display = 'block';
                return;
            }

            // Reset state
            generatedContent = '';
            isStreamRunning = true;
            previewDiv.innerHTML = '';
            errorDiv.style.display = 'none';

            // Show loading, hide form and result
            setupForm.style.display = 'none';
            loadingDiv.style.display = 'block';
            resultDiv.style.display = 'none';
            generateBtn.disabled = true;

            // Disable retry and insert buttons during generation
            updateButtonStates(true);

            console.log('Starting AI generation with prompt:', prompt);
            console.log('Stream status:', checkStreamStatus());

            try {
                const response = await fetch('/dashboard/api/ai/generate/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({
                        prompt: prompt,
                        action: action,
                        current_content: currentContent
                    })
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                // Get the reader for the stream
                const reader = response.body.getReader();
                const decoder = new TextDecoder();
                let buffer = '';
                let chunkCount = 0;

                // Hide loading and show result once streaming starts
                loadingDiv.style.display = 'none';
                resultDiv.style.display = 'block';
                updateStreamStatusUI(true);

                while (true) {
                    const { done, value } = await reader.read();

                    if (done) {
                        console.log('Stream completed after', chunkCount, 'chunks');
                        console.log('Final content length:', generatedContent.length);
                        isStreamRunning = false;
                        updateStreamStatusUI(false, true);
                        // Enable retry and insert buttons when generation completes
                        updateButtonStates(false);
                        break;
                    }

                    // Decode the chunk and add to buffer
                    buffer += decoder.decode(value, { stream: true });
                    chunkCount++;

                    // Process complete SSE messages
                    const lines = buffer.split('\n\n');
                    buffer = lines.pop() || ''; // Keep incomplete message in buffer

                    for (const line of lines) {
                        if (line.startsWith('data: ')) {
                            const data = line.slice(6).trim();

                            if (data) {
                                try {
                                    const parsed = JSON.parse(data);

                                    if (parsed.error) {
                                        console.error('AI Error:', parsed.error);
                                        errorDiv.textContent = parsed.error;
                                        errorDiv.style.display = 'block';
                                        resultDiv.style.display = 'none';
                                        setupForm.style.display = 'block';
                                        isStreamRunning = false;
                                        updateStreamStatusUI(false);
                                        break;
                                    }

                                    if (parsed.content) {
                                        generatedContent += parsed.content;

                                        // Strip markdown code blocks and render as HTML
                                        const cleanContent = stripMarkdownCodeBlocks(generatedContent);
                                        previewDiv.innerHTML = cleanContent;

                                        console.log('Received chunk #' + chunkCount + ':', parsed.content.length, 'chars');
                                        console.log('Stream status:', checkStreamStatus());

                                        // Update status UI every 5 chunks
                                        if (chunkCount % 5 === 0) {
                                            updateStreamStatusUI(true);
                                        }
                                    }

                                    if (parsed.done) {
                                        console.log('Content generation completed naturally');
                                        console.log('Final stream status:', checkStreamStatus());
                                        isStreamRunning = false;
                                        updateStreamStatusUI(false, true);
                                        // Enable retry and insert buttons when generation completes
                                        updateButtonStates(false);
                                        break;
                                    }
                                } catch (e) {
                                    console.error('Parse error:', e, 'Data:', data);
                                }
                            }
                        }
                    }
                }

                if (generatedContent && (!errorDiv.style.display || errorDiv.style.display === 'none')) {
                    console.log('Content generated successfully');
                    console.log('Preview:', generatedContent.substring(0, 200) + '...');
                }

            } catch (err) {
                console.error('Fetch Error:', err);
                errorDiv.textContent = 'Error: ' + err.message;
                errorDiv.style.display = 'block';
                loadingDiv.style.display = 'none';
                resultDiv.style.display = 'none';
                setupForm.style.display = 'block';
                isStreamRunning = false;
                updateStreamStatusUI(false);
                // Enable buttons on error
                updateButtonStates(false);
            } finally {
                generateBtn.disabled = false;
                // Ensure loading is hidden no matter what
                loadingDiv.style.display = 'none';
                // Ensure buttons are enabled in finally block
                updateButtonStates(false);
            }
        };

        // Retry button
        modal.querySelector('#ai-retry').onclick = () => {
            modal.querySelector('#ai-result').style.display = 'none';
            modal.querySelector('#ai-setup-form').style.display = 'block';
        };

        // Insert button
        modal.querySelector('#ai-insert').onclick = () => {
            const action = modal.querySelector('#ai-action').value;

            if (generatedContent) {
                console.log('Inserting content. Length:', generatedContent.length);
                console.log('Content preview:', generatedContent.substring(0, 100) + '...');

                // Strip markdown code blocks before inserting
                const cleanContent = stripMarkdownCodeBlocks(generatedContent);
                console.log('Clean content length:', cleanContent.length);

                if (action === 'edit') {
                    editor.insertContent(cleanContent);
                } else {
                    editor.setContent(cleanContent);
                }
                closeModal();
            } else {
                console.error('No content to insert!');
            }
        };
    }
});
