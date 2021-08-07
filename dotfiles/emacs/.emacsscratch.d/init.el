;; Disable the startup page
(setq inhibit-startup-message t)

(scroll-bar-mode -1)  ;; Disable visible scrollbar
(tool-bar-mode -1)  ;; Disable the toolbar
(tooltip-mode -1)  ;; Disable tooltips
(menu-bar-mode -1) ;; Disable the menu bar

(set-fringe-mode 10) ;; Give some breathing room (?)

;; <leaf-install-code>
(eval-and-compile
  (customize-set-variable
   'package-archives '(("org" . "https://orgmode.org/elpa/")
                       ("melpa" . "https://melpa.org/packages/")
                       ("gnu" . "https://elpa.gnu.org/packages/")))
  (package-initialize)
  (unless (package-installed-p 'leaf)
    (package-refresh-contents)
    (package-install 'leaf))

  (leaf leaf
    :custom ((leaf-defaults . '(:ensure t))))

  (leaf leaf-keywords
    :ensure t
    :init
    ;; optional packages if you want to use :hydra, :el-get, :blackout,,,
    ;;(leaf hydra :ensure t)
    ;;(leaf el-get :ensure t)
    ;;(leaf blackout :ensure t)

    :config
    ;; initialize leaf-keywords.el
    (leaf-keywords-init)))
;; </leaf-install-code>


;; Persist history over Emacs restarts. Vertico sorts by history position.
(leaf savehist
  :init
  (savehist-mode))

(leaf marginalia
  :after vertico
  :custom
  (marginalia-annotators '(marginalia-annotators-heavy marginalia-annotators-light nil))
  :init
  (marginalia-mode))

 ;; Use the `orderless' completion style. Additionally enable
;; `partial-completion' for file path expansion. `partial-completion' is
;; important for wildcard support. Multiple files can be opened at once
;; with `find-file' if you enter a wildcard. You may also give the
;; `initials' completion style a try.
(leaf orderless
  :init
  (setq completion-styles '(orderless)
        completion-category-defaults nil
        completion-category-overrides '((file (styles partial-completion)))))

(leaf vertico
  :init
  (vertico-mode)

  ;; Grow and shrink the Vertico minibuffer
  (setq vertico-resize t)

  ;; Optionally enable cycling for `vertico-next' and `vertico-previous'.
  (setq vertico-cycle t)
  )

(leaf consult)

(column-number-mode)			;; Display column number in the mode line
(global-display-line-numbers-mode t)	;; display line numbers globally

;; Disable line numbers for some modes
(dolist (mode '(org-mode-hook
		term-mode-hook
		eshell-mode-hook))
  (add-hook mode (lambda () (display-line-nbumbers-mode 0))))

(leaf rainbow-delimiters
  :hook (prog-mode . rainbow-delimiters-mode))

(leaf which-key
  :init (which-key-mode)
  :custom
  (which-key-idle-delay . 0.3))

(leaf monokai-theme)

(load-theme 'monokai t)

(leaf helpful
  :bind
  ([remap describe-function] . helpful-function)
  ([remap describe-variable] . helpful-variable)
  ([remap describe-symbol] . helpful-symbol)
  ([remap describe-key] . helpful-key)
  ("C-h C" . helpful-command))

(show-paren-mode 1)
(setq-default indent-tabs-mode nil)

;; We use the no-littering package to keep folders where we edit
;; files and the Emacs configuration folder clean! It knows about a
;; wide variety of variables for built in Emacs features as well as
;; those from community packages so it can be much easier than
;; finding and setting these variables yourself.
(leaf no-littering
  :config
  

  ;; no-littering doesn't set this by default so we must place
  ;; auto save files in the same path as it uses for sessions
  (setq auto-save-file-name-transforms
        `((".*" ,(no-littering-expand-var-file-name "auto-save/") t)))

  ;; Saved customizations
  ;; Emacs will save customizations into your
  ;; init.el file by default. If you don't want that, you might want
  ;; to store them in a sibling file or even in the etc/ directory:
  (setq custom-file (no-littering-expand-etc-file-name "custom.el")))

(setq require-final-newline t)
(customize-set-variable 'load-prefer-newer t)
