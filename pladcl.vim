" Vim syntax file
" Language: pladcl (plasma's lazy ass dc language)
" Maintainer: plasma

if !exists("main_syntax")
  if exists("b:current_syntax")
    finish
  endif
  let main_syntax = 'pladcl'
endif

" Keywords
syn keyword pladclBasicKeywords state interrupt function end if then return while do break for in to step stack and or not skipwhite

syn match pladclLeftParen "("
syn match pladclBacktick "`"

syn match pladclFunction "\w\+\s*(" contains=pladclLeftParen

syn match pladclComment '#.*$'

syn match pladclNumber '-\=\d\+'
syn match pladclIdentifier '([a-z][A-Z]\d)\+'
syn match pladclString '"[^"]*"'
syn match pladclDcliteral '`[^`]*`' contains=pladclBacktick
syn match pladclChar "'.'"

hi def link pladclComment Comment

hi def link pladclBasicKeywords Keyword
hi def link pladclEndKeywords Keyword

hi def link pladclFunction Function

hi def link pladclNumber Number
hi def link pladclString String
hi def link pladclDcliteral Macro
hi def link pladclChar Character
