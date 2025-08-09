--[==========================================[--
          L3BUILD FILE FOR CHAR2PATH
      Once Pushed With This File Modified
        A New Release Will Be Published
--]==========================================]--

--[==========================================[--
               Basic Information
             Do Check Before Push
--]==========================================]--

module              = "char2path"
version             = "v1.0.1"
date                = "2025-08-09"
maintainer          = "Zongping Ding, Mingyu Xia"
uploader            = "Mingyu Xia"
maintainid          = "Zongping Ding"
email               = "myhsia@outlook.com"
repository          = "https://github.com/" .. maintainid .. "/" .. module
announcement        = [[Version 1.0.1 releeased.]]
summary             = "A LaTeX package that converts characters into TikZ paths"
description         = "The char2path package provides an easy way to converts characters into TikZ paths quickly, developed by expl3 based on TikZ."

--[==========================================[--
          Build, Pack, Tag, and Upload
         Do not Modify Unless Necessary
--]==========================================]--

ctanzip             = module
cleanfiles          = {"*log", "*.pdf", "*.zip", "*.curlopt", typesetdemofiles}
excludefiles        = {"*~"}
installfiles        = {"*.sty", "*.data.tex", "*-demo.tex"}
localdir            = "./testfiles/unpacked"
textfiles           = {"*.md", "LICENSE", "*.lua"}
typesetdemofiles    = {module .. "-demo.tex"}
typesetfiles        = {module .. ".dtx"}
typesetexe          = "latexmk -lualatex"
typesetruns         = 1
uploadconfig  = {
  pkg          = module,
  version      = version .. " " .. date,
  author       = maintainer,
  uploader     = uploader,
  email        = email,
  summary      = summary,
  description  = description,
  license      = "lppl1.3c",  
  ctanPath     = "/graphics/pgf/contrib/" .. module,
  announcement = announcement,
  home         = "https://github.com/" .. maintainid,
  bugtracker   = repository .. "/issues",
  support      = repository .. "/issues",
  repository   = repository,
  development  = "https://github.com/" .. maintainid,
  update       = true,
}
function update_tag(file, content, tagname, tagdate)
  tagname = version
  tagdate = date
  if string.match(file, "%.dtx$") or string.match(file, "%.tex$") or string.match(file, "%.sty$") then
    content = string.gsub(content,
      "\\ProvidesExplPackage {" .. module .. "} %{[^}]+%} %{[^}]+%}[\r\n%s]*%{[^}]+%}",
      "\\ProvidesExplPackage {" .. module .. "} {" .. tagdate .. "} {" .. tagname .. "}\n  {" .. summary .. "}")
    content = string.gsub(content,
      "\\date{Released %d+%-%d+%-%d+\\quad \\texttt{v([%d%.A-Z]+)}}",
      "\\date{Released " .. tagdate .. "\\quad \\texttt{" .. tagname .. "}}")
  end
  return content
end

--[== "Hacks" to `l3build` | Do not Modify ==]--

function docinit_hook()
  cp(ctanreadme, unpackdir, currentdir)
  for _, demo in ipairs(typesetdemofiles) do
    cp(demo, unpackdir, currentdir)
  end
  return 0
end
function tex(file,dir,cmd)
  dir = dir or "."
  cmd = cmd or typesetexe
  if os.getenv("WINDIR") ~= nil or os.getenv("COMSPEC") ~= nil then
    upretex_aux = "-usepretex=\"" .. typesetcmds .. "\""
    makeidx_aux = "-e \"$makeindex=q/makeindex -s " .. indexstyle .. " %O %S/\""
    sandbox_aux = "set \"TEXINPUTS=../unpacked;%TEXINPUTS%;\" &&"
  else
    upretex_aux = "-usepretex=\'" .. typesetcmds .. "\'"
    makeidx_aux = "-e \'$makeindex=q/makeindex -s " .. indexstyle .. " %O %S/\'"
    sandbox_aux = "TEXINPUTS=\"../unpacked:$(kpsewhich -var-value=TEXINPUTS):\""
  end
  return run(dir, sandbox_aux .. " " .. cmd         .. " " ..
                  upretex_aux .. " " .. makeidx_aux .. " " .. file)
end