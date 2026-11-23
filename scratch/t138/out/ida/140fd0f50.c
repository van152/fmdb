__int64 __fastcall sub_140FD0F50(
        _QWORD *a1,
        __int64 a2,
        char a3,
        unsigned __int8 a4,
        unsigned __int8 a5,
        unsigned __int8 a6,
        char a7,
        unsigned int a8,
        unsigned __int8 a9,
        unsigned __int8 a10)
{
  __int64 v10; // r13
  int v12; // ecx
  unsigned __int8 v13; // r12
  int v14; // ecx
  unsigned __int8 v15; // bl
  int v16; // ecx
  int v17; // ecx
  int v18; // ecx
  int v19; // ecx
  int v20; // ecx
  int v21; // ecx
  int v22; // ecx
  int v23; // ecx
  int v24; // ecx
  int v25; // ecx
  int v26; // ecx
  int v27; // ecx
  unsigned __int8 v28; // cf
  int v29; // ecx
  int v30; // ecx
  unsigned __int8 v31; // dl
  __int64 v32; // r14
  unsigned __int8 v33; // cl
  unsigned __int8 v34; // r12
  unsigned __int8 v35; // bl
  int v36; // esi
  int *v37; // rax
  int v38; // r13d
  int v39; // ebx
  __int64 v40; // rdi
  volatile signed __int32 *v41; // r15
  unsigned int v42; // eax
  __int64 v43; // rsi
  __int64 v44; // rdx
  _BYTE *v45; // rbx
  __int64 v46; // rdi
  volatile signed __int32 *v47; // rcx
  __int64 v48; // rax
  _QWORD *v49; // rdi
  __int64 v50; // rcx
  volatile signed __int32 *v51; // rcx
  volatile signed __int32 *v52; // rcx
  volatile signed __int32 *v53; // rcx
  __int64 v54; // rcx
  volatile signed __int32 *v55; // rsi
  bool v56; // bl
  __int64 v57; // rsi
  volatile signed __int32 *v58; // rcx
  __int64 v59; // rsi
  char v60; // bl
  __int64 v61; // rax
  __int64 v62; // rcx
  int v63; // esi
  volatile signed __int32 *v64; // rax
  int v65; // r12d
  int v66; // ebx
  __int64 v67; // rdi
  volatile signed __int32 *v68; // r14
  unsigned int v69; // eax
  __int64 v70; // rsi
  __int64 v71; // rdx
  _BYTE *v72; // rbx
  volatile signed __int32 *v73; // rdi
  volatile signed __int32 *v74; // rcx
  __int64 v75; // rax
  __int64 v76; // rcx
  volatile signed __int32 *v77; // rcx
  volatile signed __int32 *v78; // rcx
  volatile signed __int32 *v79; // rcx
  __int64 v80; // rcx
  volatile signed __int32 *v81; // rsi
  bool v82; // bl
  int v83; // r12d
  volatile signed __int32 *v84; // rcx
  unsigned __int8 v85; // al
  int v86; // esi
  volatile signed __int32 *v87; // rax
  int v88; // r12d
  char v89; // bl
  int v90; // esi
  int *v91; // rax
  int v92; // r12d
  int v93; // ebx
  __int64 v94; // rdi
  volatile signed __int32 *v95; // r15
  unsigned int v96; // eax
  __int64 v97; // rsi
  __int64 v98; // rdx
  _BYTE *v99; // rbx
  volatile signed __int32 *v100; // rdi
  volatile signed __int32 *v101; // rcx
  __int64 v102; // rax
  __int64 v103; // rcx
  volatile signed __int32 *v104; // rcx
  _QWORD *v105; // rdi
  volatile signed __int32 *v106; // rcx
  volatile signed __int32 *v107; // rcx
  __int64 v108; // rcx
  volatile signed __int32 *v109; // rsi
  bool v110; // bl
  _QWORD *v111; // r12
  __int64 v112; // rsi
  volatile signed __int32 *v113; // rcx
  int v114; // esi
  volatile signed __int32 *v115; // rax
  int v116; // r12d
  int v117; // esi
  char v118; // bl
  volatile signed __int32 *v119; // rcx
  __int64 v120; // rcx
  __int64 v121; // rcx
  __int64 v122; // rcx
  __int64 v123; // rcx
  _QWORD *v124; // r13
  int v125; // ebx
  __int64 v126; // rdi
  volatile signed __int32 *v127; // r15
  unsigned int v128; // eax
  __int64 v129; // rsi
  __int64 v130; // rdx
  _BYTE *v131; // rbx
  volatile signed __int32 *v132; // rdi
  volatile signed __int32 *v133; // rcx
  __int64 v134; // rax
  __int64 v135; // rcx
  volatile signed __int32 *v136; // rcx
  volatile signed __int32 *v137; // rcx
  volatile signed __int32 *v138; // rcx
  __int64 v139; // rcx
  volatile signed __int32 *v140; // rsi
  bool v141; // bl
  char v142; // si
  volatile signed __int32 *v143; // rcx
  int v144; // esi
  volatile signed __int32 *v145; // rax
  int v146; // r12d
  int v147; // esi
  char v148; // bl
  volatile signed __int32 *v149; // rcx
  __int64 v150; // rcx
  __int64 v151; // rcx
  __int64 v152; // rcx
  int v153; // edi
  char v154; // bl
  volatile signed __int32 *v155; // rcx
  __int64 v156; // rcx
  __int64 v157; // rcx
  __int64 v158; // rcx
  __int64 v159; // rcx
  __int64 v160; // rcx
  __int64 v161; // rcx
  int v162; // ebx
  __int64 v163; // rdi
  volatile signed __int32 *v164; // r15
  unsigned int v165; // eax
  __int64 v166; // rsi
  __int64 v167; // rdx
  _BYTE *v168; // rbx
  __int64 v169; // rdi
  volatile signed __int32 *v170; // rcx
  __int64 v171; // rax
  __int64 v172; // rcx
  volatile signed __int32 *v173; // rcx
  volatile signed __int32 *v174; // rcx
  volatile signed __int32 *v175; // rcx
  __int64 v176; // rcx
  volatile signed __int32 *v177; // rsi
  bool v178; // bl
  int v179; // ecx
  volatile signed __int32 *v180; // rcx
  int v181; // esi
  int *v182; // rax
  int v183; // r12d
  __int64 v184; // rdi
  bool v185; // r13
  __int64 v186; // rax
  __int64 v187; // rsi
  unsigned __int64 v188; // rdi
  unsigned __int64 v189; // rcx
  __int64 v190; // r14
  _QWORD *v191; // rbx
  __int64 v192; // rax
  int v193; // ebx
  __int64 v194; // rdi
  volatile signed __int32 *v195; // r15
  unsigned int v196; // eax
  __int64 v197; // rsi
  __int64 v198; // rdx
  _BYTE *v199; // rbx
  volatile signed __int32 *v200; // rdi
  volatile signed __int32 *v201; // rcx
  __int64 v202; // rax
  __int64 v203; // rcx
  volatile signed __int32 *v204; // rcx
  _QWORD *v205; // rdi
  volatile signed __int32 *v206; // rcx
  volatile signed __int32 *v207; // rcx
  __int64 v208; // rcx
  volatile signed __int32 *v209; // rsi
  bool v210; // bl
  volatile signed __int32 *v211; // rcx
  int v212; // esi
  volatile signed __int32 *v213; // rax
  int v214; // r12d
  int v215; // esi
  volatile signed __int32 *v216; // rbx
  int v217; // r15d
  char v218; // r13
  volatile signed __int32 *v219; // rcx
  __int64 v220; // rcx
  _QWORD *v221; // rbx
  volatile signed __int32 *v222; // rbx
  int v223; // ebx
  __int64 v224; // rdi
  volatile signed __int32 *v225; // r15
  unsigned int v226; // eax
  __int64 v227; // rsi
  __int64 v228; // rdx
  _BYTE *v229; // rbx
  __int64 v230; // rdi
  volatile signed __int32 *v231; // rcx
  __int64 v232; // rax
  __int64 v233; // rcx
  volatile signed __int32 *v234; // rcx
  volatile signed __int32 *v235; // rcx
  volatile signed __int32 *v236; // rcx
  __int64 v237; // rcx
  volatile signed __int32 *v238; // rdi
  bool v239; // bl
  int v240; // r12d
  volatile signed __int32 *v241; // rcx
  int v242; // esi
  int *v243; // rax
  int v244; // r12d
  __int64 v245; // rax
  int v246; // esi
  unsigned int v247; // edi
  char v248; // bl
  volatile signed __int32 *v249; // rcx
  __int64 v250; // rcx
  __int64 v251; // rcx
  __int64 v252; // r15
  bool v253; // r12
  __int64 v254; // rax
  __int64 v255; // rsi
  unsigned __int64 v256; // r15
  unsigned __int64 v257; // rcx
  __int64 v258; // rdi
  bool v259; // r12
  __int64 v260; // rax
  __int64 v261; // rsi
  unsigned __int64 v262; // rdi
  unsigned __int64 v263; // rcx
  __int64 v264; // r14
  int v265; // ebx
  __int64 v266; // rdi
  unsigned int v267; // eax
  __int64 v268; // rsi
  __int64 v269; // rdx
  _BYTE *v270; // rbx
  volatile signed __int32 *v271; // rdi
  volatile signed __int32 *v272; // rcx
  __int64 v273; // rax
  __int64 v274; // rcx
  volatile signed __int32 *v275; // rcx
  volatile signed __int32 *v276; // rcx
  volatile signed __int32 *v277; // rcx
  __int64 v278; // rcx
  volatile signed __int32 *v279; // rsi
  bool v280; // bl
  volatile signed __int32 *v281; // rcx
  int v282; // esi
  int *v283; // rax
  int v284; // r12d
  int v285; // esi
  char v286; // bl
  volatile signed __int32 *v287; // rcx
  __int64 v288; // rcx
  __int64 v289; // rcx
  int v290; // ebx
  __int64 v291; // rdi
  volatile signed __int32 *v292; // r15
  unsigned int v293; // eax
  __int64 v294; // rsi
  __int64 v295; // rdx
  _BYTE *v296; // rbx
  __int64 v297; // rdi
  volatile signed __int32 *v298; // rcx
  __int64 v299; // rax
  __int64 v300; // rcx
  volatile signed __int32 *v301; // rcx
  volatile signed __int32 *v302; // rcx
  volatile signed __int32 *v303; // rcx
  __int64 v304; // rcx
  volatile signed __int32 *v305; // rsi
  bool v306; // bl
  int v307; // ecx
  volatile signed __int32 *v308; // rcx
  int v309; // esi
  int *v310; // rax
  int v311; // r12d
  __int64 v312; // r14
  __int64 v313; // rsi
  __int64 v314; // r15
  int v315; // edi
  int v316; // ebx
  volatile signed __int32 *v317; // rdi
  bool v318; // si
  __int64 v319; // rax
  __int64 v320; // rdi
  __int64 *v321; // rsi
  __int64 v322; // rax
  volatile signed __int32 *v323; // rcx
  volatile signed __int32 *v324; // r14
  __int64 v325; // rcx
  __int64 v326; // rdi
  bool v327; // r12
  __int64 v328; // rax
  __int64 v329; // rsi
  unsigned __int64 v330; // rdi
  unsigned __int64 v331; // rcx
  int v332; // esi
  char v333; // bl
  volatile signed __int32 *v334; // rcx
  __int64 v335; // rcx
  __int64 v336; // rcx
  __int64 v337; // rcx
  __int64 v338; // rcx
  __int64 v339; // rcx
  int v340; // edi
  __int64 v341; // r13
  int v342; // esi
  void (__fastcall ***v343)(_QWORD, __int64); // rcx
  __int64 v344; // r15
  __int64 *v345; // rbx
  __int64 v346; // r14
  __int64 *v347; // rax
  unsigned __int64 v348; // rsi
  __int64 v349; // rdx
  unsigned __int64 v350; // rsi
  unsigned __int64 v351; // r14
  __int64 *v352; // rdi
  __int64 v353; // rcx
  __int64 v354; // rcx
  __int64 v355; // rcx
  __int64 v356; // rcx
  unsigned __int64 v357; // rdi
  unsigned __int64 v358; // r8
  unsigned __int64 v359; // rax
  unsigned __int64 v360; // rbx
  _QWORD *v361; // r14
  __int64 v362; // rdi
  unsigned __int64 v363; // rcx
  __int64 v364; // r8
  __int64 v365; // rcx
  __int64 v366; // r14
  __int64 v367; // rcx
  bool v368; // al
  _QWORD *v369; // r15
  __int64 *v370; // rdi
  _QWORD *v371; // r15
  unsigned __int64 v372; // rax
  unsigned __int64 v373; // rcx
  unsigned __int64 v374; // rax
  __int64 v375; // rsi
  __int64 *v376; // rdi
  _QWORD *v377; // r13
  __int64 v378; // rbx
  __int64 v379; // rcx
  unsigned __int64 v380; // rcx
  __int64 v381; // r8
  __int64 v382; // r15
  bool v383; // al
  unsigned __int64 v384; // r14
  unsigned __int64 v385; // r8
  unsigned __int64 v386; // rsi
  __int64 v387; // rbx
  unsigned __int64 v388; // rsi
  __int64 *v389; // r13
  bool v390; // zf
  _QWORD *v391; // r13
  __int64 v392; // rsi
  unsigned __int64 v393; // rcx
  __int64 v394; // r8
  __int64 v395; // r15
  bool v396; // al
  __int64 *v397; // r14
  _QWORD *v398; // rdi
  __int64 v399; // rdi
  bool v400; // r12
  __int64 v401; // rsi
  unsigned __int64 v402; // rdi
  unsigned __int64 v403; // rcx
  __int64 v404; // rsi
  _QWORD *v405; // rbx
  __int64 v406; // rdi
  int v407; // edi
  int v408; // ebx
  __int64 v409; // rdi
  volatile signed __int32 *v410; // r15
  unsigned int v411; // eax
  __int64 v412; // rsi
  __int64 v413; // rdx
  _BYTE *v414; // rbx
  __int64 v415; // rdi
  volatile signed __int32 *v416; // rcx
  __int64 v417; // rax
  __int64 v418; // rcx
  volatile signed __int32 *v419; // rcx
  volatile signed __int32 *v420; // rcx
  volatile signed __int32 *v421; // rcx
  __int64 v422; // rcx
  volatile signed __int32 *v423; // rsi
  bool v424; // bl
  int v425; // ecx
  volatile signed __int32 *v426; // rcx
  int v427; // esi
  int *v428; // rax
  int v429; // r12d
  __int64 v430; // r14
  __int64 v431; // rsi
  _QWORD *v432; // rbx
  __int64 v433; // r15
  int v434; // ebx
  __int64 v435; // rcx
  __int64 v436; // rcx
  __int64 v437; // rcx
  __int64 v438; // rcx
  __int64 v439; // rax
  int v440; // edi
  unsigned int v441; // esi
  char v442; // bl
  volatile signed __int32 *v443; // rcx
  __int64 v444; // rax
  int v445; // r13d
  __int64 v446; // rdi
  void (__fastcall ***v447)(_QWORD, __int64); // rcx
  _QWORD *v448; // r15
  __int64 *v449; // rbx
  __int64 v450; // r12
  unsigned __int64 v451; // rax
  unsigned __int64 v452; // r14
  unsigned __int64 v453; // rcx
  __int64 *v454; // rdi
  __int64 v455; // rdi
  unsigned __int64 v456; // rcx
  __int64 v457; // rbx
  __int64 v458; // rbx
  bool v459; // al
  __int64 v460; // r13
  __int64 v461; // rax
  __int64 v462; // rsi
  unsigned __int64 v463; // r13
  unsigned __int64 v464; // rcx
  __int64 v465; // rax
  __int64 v466; // r12
  int v467; // esi
  void (__fastcall ***v468)(_QWORD, __int64); // rcx
  __int64 v469; // rsi
  __int64 *v470; // r15
  __int64 *v471; // rax
  unsigned __int64 v472; // rdi
  __int64 v473; // rdx
  unsigned __int64 v474; // r13
  __int64 *v475; // rbx
  __int64 v476; // rcx
  __int64 v477; // rcx
  __int64 v478; // rcx
  unsigned __int64 v479; // rbx
  unsigned __int64 v480; // rdi
  unsigned __int64 v481; // rax
  unsigned __int64 v482; // r15
  _QWORD *v483; // rbx
  __int64 v484; // r9
  unsigned __int64 v485; // rcx
  __int64 v486; // r8
  bool v487; // al
  __int64 *v488; // rbx
  _QWORD *v489; // rdi
  _QWORD *v490; // rsi
  unsigned __int64 v491; // rbx
  unsigned __int64 v492; // rcx
  unsigned __int64 v493; // rbx
  __int64 v494; // rax
  __int64 v495; // r12
  __int64 *v496; // rdi
  _QWORD *v497; // rsi
  __int64 v498; // rdi
  unsigned __int64 v499; // rcx
  __int64 v500; // r8
  bool v501; // al
  unsigned __int64 v502; // r14
  unsigned __int64 v503; // r15
  unsigned __int64 v504; // rsi
  __int64 *v505; // r12
  __int64 v506; // rdi
  unsigned __int64 v507; // rcx
  __int64 v508; // rbx
  __int64 v509; // rbx
  bool v510; // al
  unsigned __int64 v511; // rax
  _QWORD *v512; // rbx
  int v513; // ebx
  __int64 v514; // rdi
  volatile signed __int32 *v515; // r15
  unsigned int v516; // eax
  __int64 v517; // rsi
  __int64 v518; // rdx
  _BYTE *v519; // rbx
  __int64 v520; // rdi
  volatile signed __int32 *v521; // rcx
  __int64 v522; // rax
  __int64 v523; // rcx
  volatile signed __int32 *v524; // rcx
  volatile signed __int32 *v525; // rcx
  volatile signed __int32 *v526; // rcx
  __int64 v527; // rcx
  volatile signed __int32 *v528; // rsi
  bool v529; // bl
  int v530; // ecx
  volatile signed __int32 *v531; // rcx
  int v532; // esi
  int *v533; // rax
  int v534; // r12d
  __int64 v535; // rdi
  int v536; // esi
  void (__fastcall ***v537)(_QWORD, __int64); // rcx
  __int64 v538; // r12
  __int64 *v539; // r14
  __int64 v540; // r13
  __int64 *v541; // rax
  unsigned __int64 v542; // rbx
  __int64 v543; // rdx
  unsigned __int64 v544; // r15
  unsigned __int64 v545; // r13
  __int64 *v546; // rsi
  __int64 v547; // rcx
  __int64 v548; // rcx
  _QWORD *v549; // rbx
  __int64 v550; // rcx
  __int64 v551; // rcx
  __int64 v552; // rcx
  __int64 v553; // rcx
  unsigned __int64 v554; // rsi
  unsigned __int64 v555; // rbx
  unsigned __int64 v556; // rax
  unsigned __int64 v557; // r14
  _QWORD *v558; // rsi
  __int64 v559; // r9
  unsigned __int64 v560; // rcx
  __int64 v561; // r8
  __int64 v562; // rbx
  bool v563; // al
  _QWORD *v564; // rbx
  __int64 *v565; // rsi
  _QWORD *v566; // rbx
  unsigned __int64 v567; // r12
  unsigned __int64 v568; // rsi
  unsigned __int64 v569; // rcx
  unsigned __int64 v570; // rsi
  __int64 v571; // r15
  __int64 *v572; // rdi
  __int64 v573; // rdi
  unsigned __int64 v574; // rcx
  __int64 v575; // rbx
  __int64 v576; // r14
  bool v577; // al
  unsigned __int64 v578; // r13
  unsigned __int64 v579; // r14
  unsigned __int64 v580; // r12
  __int64 v581; // r13
  __int64 *v582; // rdi
  __int64 v583; // rsi
  unsigned __int64 v584; // rcx
  __int64 v585; // rdi
  __int64 v586; // rdi
  bool v587; // al
  _QWORD *v588; // rsi
  unsigned __int64 v589; // rdi
  char v590; // r12
  __int64 v591; // rax
  __int64 v592; // rsi
  unsigned __int64 v593; // rcx
  __int64 v594; // rsi
  _QWORD *v595; // rbx
  __int64 v596; // r15
  int v597; // edi
  __int64 v598; // rcx
  __int64 v599; // rcx
  __int64 v600; // rcx
  int v601; // r15d
  __int64 v602; // rdi
  void (__fastcall ***v603)(_QWORD, __int64); // rcx
  __int64 *v604; // rbx
  __int64 v605; // r13
  unsigned __int64 v606; // rax
  unsigned __int64 v607; // r12
  unsigned __int64 v608; // rcx
  unsigned __int64 v609; // r12
  __int64 *v610; // rdi
  __int64 v611; // rdi
  _QWORD *v612; // rbx
  unsigned __int64 v613; // rcx
  __int64 v614; // rbx
  bool v615; // al
  _QWORD *v616; // r13
  int v617; // ebx
  __int64 v618; // rdi
  volatile signed __int32 *v619; // r15
  unsigned int v620; // eax
  __int64 v621; // rsi
  __int64 v622; // rdx
  _BYTE *v623; // rbx
  __int64 v624; // rdi
  volatile signed __int32 *v625; // rcx
  __int64 v626; // rax
  __int64 v627; // rcx
  volatile signed __int32 *v628; // rcx
  volatile signed __int32 *v629; // rcx
  volatile signed __int32 *v630; // rcx
  __int64 v631; // rcx
  volatile signed __int32 *v632; // rsi
  bool v633; // bl
  char v634; // di
  volatile signed __int32 *v635; // rcx
  __int64 v636; // rsi
  char v637; // bl
  __int64 v638; // rax
  __int64 v639; // rcx
  __int64 v640; // rcx
  __int64 v641; // rcx
  __int64 v642; // rcx
  __int64 v643; // rcx
  __int64 v644; // rcx
  __int64 v645; // rcx
  __int64 v646; // rax
  int v647; // esi
  unsigned int v648; // edi
  char v649; // bl
  volatile signed __int32 *v650; // rcx
  __int64 v651; // rcx
  __int64 v652; // rcx
  int v653; // esi
  __int64 v654; // rbx
  void (__fastcall ***v655)(_QWORD, __int64); // rcx
  __int64 *v656; // rdi
  __int64 v657; // r12
  unsigned __int64 v658; // rax
  unsigned __int64 v659; // r15
  unsigned __int64 v660; // rcx
  unsigned __int64 v661; // r15
  __int64 *v662; // rbx
  __int64 v663; // rdi
  unsigned __int64 v664; // rcx
  __int64 v665; // rbx
  __int64 v666; // rbx
  bool v667; // al
  __int64 v668; // rdi
  bool v669; // r12
  __int64 v670; // rax
  __int64 v671; // rsi
  unsigned __int64 v672; // rdi
  unsigned __int64 v673; // rcx
  __int64 v674; // rsi
  __int64 *v675; // rbx
  __int64 v676; // r15
  int v677; // edi
  unsigned int v678; // esi
  _QWORD *v679; // rbx
  _DWORD *v680; // r15
  __int64 v681; // rsi
  __int64 v682; // rsi
  int v683; // esi
  void (__fastcall ***v684)(_QWORD, __int64); // rcx
  unsigned __int64 *v685; // r12
  unsigned __int64 *v686; // rax
  unsigned __int64 v687; // rbx
  __int64 v688; // rdx
  unsigned __int64 v689; // rsi
  __int64 *v690; // rbx
  __int64 v691; // rcx
  unsigned __int64 v692; // rdi
  unsigned __int64 v693; // r15
  _QWORD *v694; // rbx
  unsigned __int64 v695; // rax
  unsigned __int64 v696; // rbx
  _QWORD *v697; // rdi
  __int64 v698; // r8
  unsigned __int64 v699; // rcx
  __int64 v700; // rdi
  bool v701; // al
  char *v702; // rbx
  _QWORD *v703; // rsi
  unsigned __int64 v704; // r15
  unsigned __int64 v705; // rcx
  unsigned __int64 v706; // r15
  __int64 v707; // rbx
  __int64 v708; // rdi
  unsigned __int64 v709; // rcx
  __int64 v710; // rsi
  bool v711; // al
  unsigned __int64 v712; // r14
  _QWORD *v713; // rdi
  unsigned __int64 v714; // r15
  unsigned __int64 v715; // r12
  __int64 v716; // rbx
  unsigned __int64 v717; // rcx
  __int64 v718; // rdi
  __int64 v719; // rsi
  bool v720; // al
  int v721; // ebx
  __int64 v722; // rdi
  volatile signed __int32 *v723; // r15
  unsigned int v724; // eax
  __int64 v725; // rsi
  __int64 v726; // rdx
  _BYTE *v727; // rbx
  __int64 v728; // rdi
  volatile signed __int32 *v729; // rcx
  __int64 v730; // rax
  __int64 v731; // rcx
  volatile signed __int32 *v732; // rcx
  _QWORD *v733; // rdi
  volatile signed __int32 *v734; // rcx
  volatile signed __int32 *v735; // rcx
  __int64 v736; // rcx
  volatile signed __int32 *v737; // rsi
  bool v738; // bl
  unsigned __int64 v739; // r12
  __int64 v740; // rax
  int v741; // esi
  unsigned int v742; // edi
  char v743; // bl
  volatile signed __int32 *v744; // rcx
  __int64 v745; // rcx
  __int64 v746; // rcx
  __int64 v747; // rcx
  __int64 v748; // rdi
  bool v749; // r12
  __int64 v750; // rsi
  unsigned __int64 v751; // rdi
  unsigned __int64 v752; // rcx
  __int64 v753; // rsi
  __int64 v754; // r15
  int v755; // esi
  __int64 v756; // rcx
  _QWORD *v757; // rdi
  int v758; // r12d
  _QWORD *v759; // rbx
  __int64 v760; // rsi
  __int64 v761; // rsi
  void (__fastcall ***v762)(_QWORD, __int64); // rcx
  _QWORD *v763; // rdi
  __int64 v764; // r14
  unsigned __int64 v765; // rax
  unsigned __int64 v766; // r15
  unsigned __int64 v767; // rcx
  unsigned __int64 v768; // r15
  __int64 v769; // r12
  _QWORD *v770; // rbx
  __int64 v771; // rdi
  unsigned __int64 v772; // rbx
  unsigned __int64 v773; // rcx
  __int64 v774; // rbx
  __int64 v775; // r12
  bool v776; // al
  int v777; // esi
  void (__fastcall ***v778)(_QWORD, __int64); // rcx
  __int64 v779; // rsi
  __int64 v780; // r8
  __int64 *v781; // r15
  __int64 v782; // r12
  __int64 *v783; // rax
  unsigned __int64 v784; // rdi
  __int64 v785; // rdx
  unsigned __int64 v786; // rdi
  unsigned __int64 v787; // r12
  __int64 *v788; // rbx
  __int64 v789; // rcx
  __int64 v790; // rcx
  unsigned __int64 v791; // rbx
  unsigned __int64 v792; // r8
  __int64 *v793; // r13
  unsigned __int64 v794; // rax
  unsigned __int64 v795; // r13
  __int64 *v796; // rbx
  __int64 v797; // r9
  unsigned __int64 v798; // rcx
  __int64 v799; // r8
  __int64 v800; // r15
  bool v801; // al
  __int64 *v802; // rbx
  _QWORD *v803; // rax
  signed __int64 v804; // r8
  unsigned __int64 v805; // rbx
  unsigned __int64 v806; // rcx
  unsigned __int64 v807; // rbx
  __int64 v808; // rsi
  __int64 *v809; // rdi
  __int64 v810; // r15
  __int64 v811; // rdi
  unsigned __int64 v812; // rcx
  __int64 v813; // r8
  bool v814; // al
  unsigned __int64 v815; // r12
  unsigned __int64 v816; // r15
  unsigned __int64 v817; // rsi
  __int64 v818; // r12
  __int64 *v819; // r14
  __int64 v820; // rdi
  unsigned __int64 v821; // rcx
  __int64 v822; // rbx
  __int64 v823; // rbx
  bool v824; // al
  __int64 *v825; // rsi
  int v826; // esi
  unsigned int v827; // edi
  char v828; // bl
  volatile signed __int32 *v829; // rcx
  __int64 v830; // rcx
  __int64 v831; // rcx
  __int64 v832; // rcx
  __int64 v833; // rcx
  __int64 v834; // rsi
  _QWORD *v835; // rbx
  __int64 v836; // r15
  __int64 v837; // rbx
  _DWORD *v838; // r13
  volatile signed __int32 *v839; // rsi
  __int64 v840; // r14
  unsigned __int64 *v841; // rbx
  __int64 v842; // r12
  unsigned __int64 *v843; // rax
  __int64 v844; // rdx
  unsigned __int64 v845; // r15
  unsigned __int64 v846; // r12
  _QWORD *v847; // rsi
  __int64 v848; // rcx
  unsigned __int64 v849; // r13
  _QWORD *v850; // rsi
  unsigned __int64 v851; // r15
  unsigned __int64 v852; // rdi
  unsigned __int64 v853; // rcx
  __int64 v854; // r14
  __int64 v855; // rbx
  unsigned __int64 v856; // rcx
  __int64 v857; // rsi
  __int64 v858; // r12
  bool v859; // al
  unsigned __int64 v860; // r12
  unsigned __int64 v861; // rsi
  __int64 v862; // r14
  __int64 v863; // rbx
  __int64 v864; // rbx
  unsigned __int64 v865; // rcx
  bool v866; // al
  _QWORD *v867; // rsi
  unsigned __int64 v868; // rax
  unsigned __int64 v869; // rbx
  __int64 v870; // rsi
  unsigned __int64 v871; // rcx
  __int64 v872; // rdi
  __int64 v873; // r12
  bool v874; // al
  unsigned __int64 *v875; // r14
  __int64 v876; // r12
  int v877; // ebx
  void (__fastcall ***v878)(_QWORD, __int64); // rcx
  _QWORD *v879; // rdi
  __int64 v880; // r15
  __int64 *v881; // r13
  __int64 v882; // r14
  __int64 *v883; // rax
  unsigned __int64 v884; // rbx
  __int64 v885; // rdx
  unsigned __int64 v886; // rsi
  unsigned __int64 v887; // r14
  __int64 *v888; // rdi
  __int64 v889; // rcx
  __int64 v890; // rcx
  _QWORD *v891; // rbx
  unsigned __int64 v892; // rdi
  unsigned __int64 v893; // rbx
  unsigned __int64 v894; // rax
  unsigned __int64 v895; // r13
  _QWORD *v896; // rdi
  __int64 v897; // r9
  unsigned __int64 v898; // rcx
  __int64 v899; // r8
  __int64 v900; // r14
  bool v901; // al
  _QWORD *v902; // r15
  __int64 *v903; // rbx
  _QWORD *v904; // rdi
  unsigned __int64 v905; // rsi
  unsigned __int64 v906; // rcx
  unsigned __int64 v907; // rsi
  __int64 v908; // rax
  __int64 v909; // r12
  __int64 *v910; // rbx
  __int64 v911; // rdi
  unsigned __int64 v912; // rcx
  __int64 v913; // rbx
  __int64 v914; // rbx
  bool v915; // al
  unsigned __int64 v916; // r14
  unsigned __int64 v917; // r13
  unsigned __int64 v918; // r15
  __int64 v919; // r14
  __int64 *v920; // r12
  __int64 v921; // rsi
  unsigned __int64 v922; // rcx
  __int64 v923; // rdi
  __int64 v924; // rbx
  bool v925; // al
  _QWORD *v926; // rdi
  __int64 v927; // rcx
  __int64 v928; // rcx
  unsigned int v929; // r12d
  __int64 v930; // rbx
  int v931; // esi
  void (__fastcall ***v932)(_QWORD, __int64); // rcx
  __int64 v933; // r12
  unsigned __int64 v934; // rax
  unsigned __int64 v935; // r15
  unsigned __int64 v936; // rcx
  unsigned __int64 v937; // r15
  __int64 v938; // rsi
  __int64 v939; // rbx
  __int64 v940; // rbx
  unsigned __int64 v941; // rcx
  __int64 v942; // r8
  bool v943; // al
  int v944; // ebx
  volatile signed __int32 *v945; // rsi
  char v946; // si
  volatile signed __int32 *v947; // rcx
  __int64 v948; // rcx
  __int64 v949; // rdi
  bool v950; // r12
  __int64 v951; // rsi
  unsigned __int64 v952; // rdi
  unsigned __int64 v953; // rcx
  __int64 v954; // rsi
  _QWORD *v955; // rbx
  __int64 v956; // r15
  int v957; // esi
  __int64 v958; // rcx
  __int64 v959; // rcx
  int v960; // r15d
  __int64 v961; // rbx
  int v962; // edi
  void (__fastcall ***v963)(_QWORD, __int64); // rcx
  __int64 *v964; // rsi
  __int64 v965; // r12
  unsigned __int64 v966; // rax
  unsigned __int64 v967; // r14
  unsigned __int64 v968; // rcx
  __int64 v969; // rdi
  __int64 *v970; // rbx
  __int64 v971; // rsi
  __int64 v972; // rdi
  unsigned __int64 v973; // rcx
  __int64 v974; // rbx
  __int64 v975; // rbx
  bool v976; // al
  __int64 v977; // rdi
  bool v978; // r12
  __int64 v979; // rsi
  unsigned __int64 v980; // rdi
  unsigned __int64 v981; // rcx
  __int64 v982; // rsi
  _QWORD *v983; // rbx
  __int64 v984; // r15
  int v985; // edi
  unsigned int v986; // esi
  __int64 v987; // rdi
  void (__fastcall ***v988)(_QWORD, __int64); // rcx
  _QWORD *v989; // rax
  __int64 v990; // r15
  __int64 *v991; // r12
  __int64 v992; // r13
  __int64 *v993; // rax
  unsigned __int64 v994; // rsi
  __int64 v995; // rdx
  unsigned __int64 v996; // rbx
  unsigned __int64 v997; // r13
  __int64 *v998; // rsi
  __int64 v999; // rcx
  __int64 v1000; // rcx
  _QWORD *v1001; // r12
  __int64 v1002; // rcx
  __int64 v1003; // rcx
  __int64 v1004; // rcx
  unsigned __int64 v1005; // rsi
  unsigned __int64 v1006; // r8
  unsigned __int64 v1007; // rax
  unsigned __int64 v1008; // r12
  _QWORD *v1009; // r13
  __int64 v1010; // rax
  unsigned __int64 v1011; // rcx
  __int64 v1012; // r8
  __int64 v1013; // rsi
  bool v1014; // al
  __int64 *v1015; // r15
  _QWORD *v1016; // rsi
  _QWORD *v1017; // rsi
  unsigned __int64 v1018; // rax
  unsigned __int64 v1019; // rcx
  unsigned __int64 v1020; // rax
  __int64 v1021; // rsi
  __int64 *v1022; // rdi
  __int64 v1023; // rbx
  __int64 v1024; // rsi
  unsigned __int64 v1025; // rcx
  __int64 v1026; // rdi
  __int64 v1027; // rdi
  bool v1028; // al
  unsigned __int64 v1029; // r13
  unsigned __int64 v1030; // r12
  __int64 v1031; // r13
  __int64 *v1032; // rdi
  __int64 v1033; // rdi
  unsigned __int64 v1034; // rcx
  __int64 v1035; // rbx
  __int64 v1036; // rbx
  bool v1037; // al
  __int64 *v1038; // r15
  _QWORD *v1039; // rsi
  __int64 v1040; // rcx
  int v1041; // ebx
  __int64 v1042; // rdi
  volatile signed __int32 *v1043; // rsi
  __int64 v1044; // r12
  unsigned __int64 v1045; // rax
  unsigned __int64 v1046; // r15
  unsigned __int64 v1047; // rcx
  unsigned __int64 v1048; // r15
  __int64 v1049; // rsi
  __int64 v1050; // rdi
  __int64 v1051; // rdi
  unsigned __int64 v1052; // rcx
  __int64 v1053; // r8
  bool v1054; // al
  __int64 v1055; // rdi
  bool v1056; // r15
  __int64 v1057; // rax
  __int64 v1058; // rbx
  unsigned __int64 v1059; // rdi
  unsigned __int64 v1060; // rcx
  _QWORD *v1061; // rsi
  __int64 v1062; // rax
  __int64 v1063; // rcx
  __int64 v1064; // rcx
  __int64 v1065; // rcx
  __int64 v1066; // rcx
  __int64 v1067; // rcx
  int v1068; // ebx
  __int64 v1069; // rdi
  void (__fastcall ***v1070)(_QWORD, __int64); // rcx
  __int64 *v1071; // rsi
  __int64 v1072; // r15
  unsigned __int64 v1073; // r12
  unsigned __int64 v1074; // rcx
  unsigned __int64 v1075; // r12
  __int64 v1076; // rbx
  __int64 *v1077; // rdi
  __int64 v1078; // r15
  __int64 v1079; // rsi
  unsigned __int64 v1080; // rcx
  __int64 v1081; // rdi
  __int64 v1082; // rdi
  bool v1083; // al
  int v1084; // edi
  int v1085; // esi
  void (__fastcall ***v1086)(_QWORD, __int64); // rcx
  __int64 v1087; // rsi
  __int64 v1088; // r8
  __int64 *v1089; // r15
  __int64 v1090; // r12
  __int64 *v1091; // rax
  unsigned __int64 v1092; // rdi
  __int64 v1093; // rdx
  unsigned __int64 v1094; // r13
  unsigned __int64 v1095; // r12
  __int64 v1096; // rbx
  unsigned __int64 v1097; // rbx
  unsigned __int64 v1098; // rdi
  unsigned __int64 v1099; // rax
  unsigned __int64 v1100; // r15
  _QWORD *v1101; // rbx
  __int64 v1102; // r9
  unsigned __int64 v1103; // rcx
  __int64 v1104; // r8
  __int64 v1105; // rdi
  bool v1106; // al
  __int64 *v1107; // rbx
  _QWORD *v1108; // rdi
  _QWORD *v1109; // rax
  signed __int64 v1110; // r8
  unsigned __int64 v1111; // rbx
  unsigned __int64 v1112; // rcx
  unsigned __int64 v1113; // rbx
  __int64 v1114; // rsi
  __int64 *v1115; // rdi
  __int64 v1116; // r15
  __int64 v1117; // r9
  unsigned __int64 v1118; // rcx
  __int64 v1119; // r8
  bool v1120; // al
  unsigned __int64 v1121; // r12
  unsigned __int64 v1122; // r15
  unsigned __int64 v1123; // rsi
  __int64 v1124; // r12
  __int64 v1125; // rbx
  unsigned __int64 v1126; // rcx
  __int64 v1127; // rdi
  bool v1128; // al
  _QWORD *v1129; // rbx
  __int64 v1130; // r13
  bool v1131; // r12
  __int64 v1132; // rax
  __int64 v1133; // rsi
  unsigned __int64 v1134; // r13
  unsigned __int64 v1135; // rcx
  __int64 v1136; // rbx
  __int64 v1137; // rax
  __int64 v1138; // rsi
  _QWORD *v1139; // rbx
  __int64 v1140; // r15
  int v1141; // edi
  unsigned int v1142; // esi
  unsigned int v1143; // r12d
  __int64 v1144; // rbx
  int v1145; // esi
  void (__fastcall ***v1146)(_QWORD, __int64); // rcx
  __int64 v1147; // r12
  unsigned __int64 v1148; // rax
  unsigned __int64 v1149; // r15
  unsigned __int64 v1150; // rcx
  unsigned __int64 v1151; // r15
  __int64 v1152; // rsi
  __int64 v1153; // rbx
  __int64 v1154; // rbx
  unsigned __int64 v1155; // rcx
  __int64 v1156; // r8
  bool v1157; // al
  __int64 v1158; // rsi
  _QWORD *v1159; // rbx
  __int64 v1160; // r15
  int v1161; // edi
  unsigned int v1162; // esi
  int v1163; // esi
  void (__fastcall ***v1164)(_QWORD, __int64); // rcx
  __int64 v1165; // rsi
  __int64 v1166; // r8
  __int64 *v1167; // r15
  __int64 v1168; // r12
  __int64 *v1169; // rax
  unsigned __int64 v1170; // rdi
  __int64 v1171; // rdx
  unsigned __int64 v1172; // rdi
  unsigned __int64 v1173; // r12
  __int64 *v1174; // rbx
  __int64 v1175; // rcx
  __int64 v1176; // rcx
  unsigned __int64 v1177; // rbx
  unsigned __int64 v1178; // r8
  _QWORD *v1179; // r13
  unsigned __int64 v1180; // rax
  unsigned __int64 v1181; // r13
  _QWORD *v1182; // rbx
  __int64 v1183; // r9
  unsigned __int64 v1184; // rcx
  __int64 v1185; // r8
  __int64 v1186; // r15
  bool v1187; // al
  __int64 *v1188; // rbx
  _QWORD *v1189; // rax
  signed __int64 v1190; // r8
  unsigned __int64 v1191; // rbx
  unsigned __int64 v1192; // rcx
  unsigned __int64 v1193; // rbx
  __int64 v1194; // rsi
  __int64 *v1195; // rdi
  __int64 v1196; // r15
  __int64 v1197; // rdi
  unsigned __int64 v1198; // rcx
  __int64 v1199; // r8
  bool v1200; // al
  unsigned __int64 v1201; // r12
  unsigned __int64 v1202; // r15
  unsigned __int64 v1203; // rsi
  __int64 v1204; // r12
  __int64 *v1205; // r14
  __int64 v1206; // rdi
  unsigned __int64 v1207; // rcx
  __int64 v1208; // rbx
  __int64 v1209; // rbx
  bool v1210; // al
  __int64 *v1211; // rsi
  __int64 v1212; // rbx
  __int64 v1213; // r12
  int v1214; // ebx
  unsigned int v1215; // r13d
  __int64 v1216; // rcx
  __int64 v1217; // rcx
  unsigned int v1218; // r12d
  __int64 v1219; // rbx
  int v1220; // esi
  void (__fastcall ***v1221)(_QWORD, __int64); // rcx
  __int64 v1222; // r12
  unsigned __int64 v1223; // rax
  unsigned __int64 v1224; // r15
  unsigned __int64 v1225; // rcx
  unsigned __int64 v1226; // r15
  __int64 v1227; // rsi
  __int64 v1228; // rbx
  __int64 v1229; // rbx
  unsigned __int64 v1230; // rcx
  __int64 v1231; // r8
  bool v1232; // al
  int v1233; // esi
  void (__fastcall ***v1234)(_QWORD, __int64); // rcx
  __int64 v1235; // rsi
  __int64 v1236; // r8
  __int64 *v1237; // r15
  __int64 v1238; // r12
  __int64 *v1239; // rax
  unsigned __int64 v1240; // rdi
  __int64 v1241; // rdx
  unsigned __int64 v1242; // rdi
  unsigned __int64 v1243; // r12
  __int64 *v1244; // rbx
  __int64 v1245; // rcx
  __int64 v1246; // rcx
  __int64 v1247; // rcx
  unsigned __int64 v1248; // rbx
  unsigned __int64 v1249; // r8
  _QWORD *v1250; // r13
  unsigned __int64 v1251; // rax
  unsigned __int64 v1252; // r13
  _QWORD *v1253; // rbx
  __int64 v1254; // r9
  unsigned __int64 v1255; // rcx
  __int64 v1256; // r8
  __int64 v1257; // r15
  bool v1258; // al
  __int64 *v1259; // rbx
  _QWORD *v1260; // rax
  signed __int64 v1261; // r8
  unsigned __int64 v1262; // rbx
  unsigned __int64 v1263; // rcx
  unsigned __int64 v1264; // rbx
  __int64 v1265; // rsi
  __int64 *v1266; // rdi
  __int64 v1267; // r15
  __int64 v1268; // rdi
  unsigned __int64 v1269; // rcx
  __int64 v1270; // r8
  bool v1271; // al
  unsigned __int64 v1272; // r12
  unsigned __int64 v1273; // r15
  unsigned __int64 v1274; // rsi
  __int64 v1275; // r12
  __int64 *v1276; // r14
  __int64 v1277; // rdi
  unsigned __int64 v1278; // rcx
  __int64 v1279; // rbx
  __int64 v1280; // rbx
  bool v1281; // al
  __int64 *v1282; // rsi
  __int64 v1283; // rbx
  __int64 v1284; // rsi
  __int64 v1285; // r15
  int v1286; // edi
  _QWORD *v1287; // r12
  char v1288; // si
  void (__fastcall ***v1289)(_QWORD, __int64); // rcx
  __int64 v1290; // rsi
  _QWORD *v1291; // r15
  __int64 v1292; // r13
  _QWORD *v1293; // rax
  unsigned __int64 v1294; // rbx
  __int64 v1295; // rdx
  unsigned __int64 v1296; // r14
  unsigned __int64 v1297; // r13
  __int64 *v1298; // rbx
  __int64 v1299; // rcx
  __int64 v1300; // rcx
  _QWORD *v1301; // rdi
  __int64 v1302; // rcx
  __int64 v1303; // rcx
  unsigned __int64 v1304; // rbx
  unsigned __int64 v1305; // rdi
  unsigned __int64 v1306; // rax
  unsigned __int64 v1307; // r15
  _QWORD *v1308; // rbx
  __int64 v1309; // rdi
  unsigned __int64 v1310; // rcx
  __int64 v1311; // rbx
  __int64 v1312; // r13
  bool v1313; // al
  char *v1314; // rbx
  _QWORD *v1315; // rdi
  unsigned __int64 v1316; // rbx
  unsigned __int64 v1317; // rcx
  unsigned __int64 v1318; // rbx
  __int64 v1319; // rax
  __int64 v1320; // r12
  _QWORD *v1321; // rdi
  __int64 v1322; // rdi
  unsigned __int64 v1323; // rcx
  __int64 v1324; // r8
  __int64 v1325; // r15
  bool v1326; // al
  unsigned __int64 v1327; // r13
  unsigned __int64 v1328; // r15
  __int64 v1329; // rsi
  char *v1330; // r12
  __int64 v1331; // rbx
  _QWORD *v1332; // r14
  unsigned __int64 v1333; // rcx
  __int64 v1334; // rdi
  __int64 v1335; // r12
  bool v1336; // al
  _QWORD *v1337; // rbx
  __int64 v1338; // rcx
  __int64 v1339; // rcx
  __int64 v1340; // rcx
  unsigned int v1341; // r12d
  __int64 v1342; // rbx
  int v1343; // esi
  void (__fastcall ***v1344)(_QWORD, __int64); // rcx
  __int64 v1345; // r12
  unsigned __int64 v1346; // rax
  unsigned __int64 v1347; // r15
  unsigned __int64 v1348; // rcx
  unsigned __int64 v1349; // r15
  __int64 v1350; // rsi
  __int64 v1351; // rbx
  __int64 v1352; // rbx
  unsigned __int64 v1353; // rcx
  __int64 v1354; // r8
  bool v1355; // al
  __int64 v1356; // rcx
  __int64 v1357; // rcx
  __int64 v1358; // rcx
  __int64 v1359; // rcx
  int v1360; // esi
  unsigned int v1361; // r13d
  _QWORD *v1362; // rbx
  void (__fastcall ***v1363)(_QWORD, __int64); // rcx
  _QWORD *v1364; // r12
  __int64 v1365; // r13
  unsigned __int64 v1366; // rax
  unsigned __int64 v1367; // r15
  unsigned __int64 v1368; // rcx
  unsigned __int64 v1369; // r15
  __int64 v1370; // rsi
  _QWORD *v1371; // rbx
  __int64 v1372; // r12
  __int64 v1373; // rbx
  _QWORD *v1374; // rdi
  unsigned __int64 v1375; // rcx
  __int64 v1376; // r8
  __int64 v1377; // r14
  bool v1378; // al
  __int64 v1379; // r13
  __int64 v1380; // rsi
  int v1381; // esi
  void (__fastcall ***v1382)(_QWORD, __int64); // rcx
  __int64 *v1383; // r12
  __int64 v1384; // rbx
  __int64 *v1385; // rax
  unsigned __int64 v1386; // rdi
  __int64 v1387; // rdx
  unsigned __int64 v1388; // r15
  unsigned __int64 v1389; // rbx
  __int64 v1390; // rsi
  __int64 v1391; // rcx
  unsigned __int64 v1392; // rsi
  unsigned __int64 v1393; // rdi
  unsigned __int64 v1394; // rax
  unsigned __int64 v1395; // r12
  _QWORD *v1396; // rsi
  __int64 v1397; // rsi
  unsigned __int64 v1398; // rcx
  __int64 v1399; // rbx
  __int64 v1400; // rbx
  bool v1401; // al
  _QWORD *v1402; // r15
  _QWORD *v1403; // rsi
  unsigned __int64 v1404; // r14
  unsigned __int64 v1405; // rcx
  __int64 v1406; // rsi
  __int64 *v1407; // rdi
  __int64 v1408; // rdi
  unsigned __int64 v1409; // rcx
  __int64 v1410; // rbx
  __int64 v1411; // rbx
  bool v1412; // al
  unsigned __int64 v1413; // rbx
  unsigned __int64 v1414; // r12
  __int64 v1415; // rdi
  __int64 v1416; // rbx
  __int64 v1417; // rbx
  unsigned __int64 v1418; // rcx
  __int64 v1419; // r8
  bool v1420; // al
  _QWORD *v1421; // rsi
  _QWORD *v1422; // rcx
  __int64 v1423; // rcx
  int v1424; // ebx
  __int64 v1425; // rdi
  __int64 v1426; // rsi
  int v1427; // esi
  void (__fastcall ***v1428)(_QWORD, __int64); // rcx
  __int64 *v1429; // r15
  unsigned __int64 v1430; // rax
  unsigned __int64 v1431; // r12
  unsigned __int64 v1432; // rcx
  _QWORD *v1433; // rsi
  __int64 v1434; // rbx
  __int64 *v1435; // rdi
  __int64 v1436; // rdi
  unsigned __int64 v1437; // rcx
  __int64 v1438; // rsi
  bool v1439; // al
  volatile signed __int32 *v1440; // rcx
  int v1441; // esi
  int *v1442; // rax
  int v1443; // r12d
  _QWORD *v1444; // r13
  int v1445; // ebx
  __int64 v1446; // rdi
  volatile signed __int32 *v1447; // r15
  unsigned int v1448; // eax
  __int64 v1449; // rsi
  __int64 v1450; // rdx
  _BYTE *v1451; // rbx
  __int64 v1452; // rdi
  volatile signed __int32 *v1453; // rcx
  __int64 v1454; // rax
  __int64 v1455; // rcx
  volatile signed __int32 *v1456; // rcx
  volatile signed __int32 *v1457; // rcx
  volatile signed __int32 *v1458; // rcx
  __int64 v1459; // rcx
  volatile signed __int32 *v1460; // rsi
  bool v1461; // bl
  unsigned __int64 v1462; // r12
  volatile signed __int32 *v1463; // rcx
  char v1464; // bl
  __int64 v1465; // rsi
  char v1466; // di
  __int64 v1467; // rax
  __int64 v1468; // rcx
  __int64 v1469; // rsi
  char v1470; // bl
  __int64 v1471; // rax
  __int64 v1472; // rcx
  int v1474; // edi
  unsigned int v1475; // r12d
  char v1476; // bl
  volatile signed __int32 *v1477; // rcx
  __int64 v1478; // rcx
  __int64 v1479; // rcx
  __int64 v1480; // rdi
  bool v1481; // r12
  __int64 v1482; // rax
  __int64 v1483; // rsi
  unsigned __int64 v1484; // rdi
  unsigned __int64 v1485; // rcx
  __int64 v1486; // rsi
  _QWORD *v1487; // rbx
  __int64 v1488; // r15
  int v1489; // eax
  unsigned int v1490; // ebx
  int v1491; // esi
  void (__fastcall ***v1492)(_QWORD, __int64); // rcx
  __int64 v1493; // r13
  __int64 *v1494; // rbx
  __int64 v1495; // r12
  __int64 *v1496; // rax
  unsigned __int64 v1497; // rdi
  __int64 v1498; // rdx
  unsigned __int64 v1499; // r15
  unsigned __int64 v1500; // r12
  __int64 v1501; // rdi
  __int64 v1502; // rcx
  __int64 v1503; // rcx
  _QWORD *v1504; // rsi
  unsigned __int64 v1505; // rsi
  unsigned __int64 v1506; // rdi
  unsigned __int64 v1507; // rax
  unsigned __int64 v1508; // rbx
  _QWORD *v1509; // rdi
  __int64 v1510; // rdi
  unsigned __int64 v1511; // rcx
  __int64 v1512; // r8
  __int64 v1513; // r12
  bool v1514; // al
  __int64 *v1515; // rsi
  unsigned __int64 v1516; // rax
  unsigned __int64 v1517; // rcx
  unsigned __int64 v1518; // rax
  __int64 v1519; // rdi
  __int64 v1520; // r15
  __int64 *v1521; // rsi
  __int64 v1522; // r9
  unsigned __int64 v1523; // rcx
  __int64 v1524; // r8
  bool v1525; // al
  unsigned __int64 v1526; // r12
  unsigned __int64 v1527; // rbx
  __int64 v1528; // r12
  __int64 *v1529; // rdi
  __int64 v1530; // rdi
  unsigned __int64 v1531; // rcx
  __int64 v1532; // r8
  bool v1533; // al
  _QWORD *v1534; // rax
  _QWORD *v1535; // rcx
  __int64 v1536; // rcx
  __int64 v1537; // rcx
  int v1538; // esi
  __int64 v1539; // rdi
  void (__fastcall ***v1540)(_QWORD, __int64); // rcx
  __int64 *v1541; // rbx
  __int64 v1542; // r14
  unsigned __int64 v1543; // rax
  unsigned __int64 v1544; // r12
  unsigned __int64 v1545; // rcx
  __int64 v1546; // r15
  __int64 *v1547; // rdi
  __int64 v1548; // rdi
  unsigned __int64 v1549; // rcx
  __int64 v1550; // rbx
  __int64 v1551; // rbx
  bool v1552; // al
  __int64 v1553; // [rsp+38h] [rbp-48h]
  unsigned __int64 v1554; // [rsp+40h] [rbp-40h]
  unsigned __int8 v1555; // [rsp+48h] [rbp-38h]
  unsigned __int64 v1556; // [rsp+48h] [rbp-38h]
  unsigned __int8 v1557; // [rsp+50h] [rbp-30h]
  unsigned __int64 v1558; // [rsp+50h] [rbp-30h]
  unsigned __int64 v1559; // [rsp+58h] [rbp-28h]
  unsigned __int64 v1560; // [rsp+58h] [rbp-28h]
  unsigned __int8 v1561; // [rsp+67h] [rbp-19h]
  unsigned __int8 v1562; // [rsp+68h] [rbp-18h]
  unsigned __int8 v1563; // [rsp+69h] [rbp-17h]
  unsigned __int8 v1564; // [rsp+6Ah] [rbp-16h]
  unsigned __int8 v1565; // [rsp+6Bh] [rbp-15h]
  unsigned __int8 v1566; // [rsp+6Ch] [rbp-14h]
  unsigned __int8 v1567; // [rsp+6Dh] [rbp-13h]
  unsigned __int8 v1568; // [rsp+6Eh] [rbp-12h]
  unsigned __int8 v1569; // [rsp+6Fh] [rbp-11h]
  char v1571; // [rsp+70h] [rbp-10h]
  char v1572; // [rsp+70h] [rbp-10h]
  unsigned __int8 v1573; // [rsp+78h] [rbp-8h]
  unsigned __int64 v1574; // [rsp+78h] [rbp-8h]
  int v1575; // [rsp+80h] [rbp+0h]
  unsigned __int64 v1576; // [rsp+80h] [rbp+0h]
  unsigned __int64 v1577; // [rsp+80h] [rbp+0h]
  int v1578; // [rsp+80h] [rbp+0h]
  volatile signed __int32 *v1579; // [rsp+88h] [rbp+8h] BYREF
  char v1580; // [rsp+90h] [rbp+10h]
  char v1581; // [rsp+91h] [rbp+11h]
  unsigned __int64 v1582; // [rsp+98h] [rbp+18h]
  __int64 v1583; // [rsp+A0h] [rbp+20h] BYREF
  unsigned __int64 v1584; // [rsp+A8h] [rbp+28h]
  unsigned __int64 v1585; // [rsp+B0h] [rbp+30h]
  int v1586; // [rsp+BCh] [rbp+3Ch] BYREF
  _QWORD v1587[4]; // [rsp+C0h] [rbp+40h] BYREF
  __int128 v1588; // [rsp+E0h] [rbp+60h] BYREF
  __int64 v1589; // [rsp+F0h] [rbp+70h] BYREF
  int v1590; // [rsp+F8h] [rbp+78h]
  int v1591; // [rsp+FCh] [rbp+7Ch]
  char v1592; // [rsp+100h] [rbp+80h]
  __int64 v1593; // [rsp+108h] [rbp+88h] BYREF
  int v1594; // [rsp+114h] [rbp+94h] BYREF
  volatile signed __int32 *v1595; // [rsp+118h] [rbp+98h] BYREF
  volatile signed __int32 *v1596; // [rsp+120h] [rbp+A0h] BYREF
  unsigned __int64 v1597; // [rsp+128h] [rbp+A8h]
  unsigned __int64 v1598; // [rsp+130h] [rbp+B0h]
  unsigned __int64 v1599; // [rsp+138h] [rbp+B8h]
  volatile signed __int32 *v1600; // [rsp+140h] [rbp+C0h] BYREF
  unsigned __int8 v1601; // [rsp+14Fh] [rbp+CFh]
  volatile signed __int32 *v1602; // [rsp+150h] [rbp+D0h] BYREF
  _QWORD *v1603; // [rsp+158h] [rbp+D8h]
  int v1604; // [rsp+160h] [rbp+E0h]
  unsigned __int8 v1605; // [rsp+167h] [rbp+E7h]
  __int64 v1606; // [rsp+168h] [rbp+E8h]

  v1606 = -2;
  v1601 = a4;
  LOBYTE(v1597) = a3;
  LOBYTE(v10) = (unsigned __int8)a8 < 0x13u;
  v12 = 262177;
  v13 = _bittest(&v12, a8);
  v14 = 264193;
  v15 = _bittest(&v14, a8);
  v16 = 266241;
  v1568 = _bittest(&v16, a8);
  v17 = 262209;
  LOBYTE(v1599) = _bittest(&v17, a8);
  v18 = 262161;
  LOBYTE(v1598) = _bittest(&v18, a8);
  v19 = 262657;
  LOBYTE(v1584) = _bittest(&v19, a8);
  v20 = 262273;
  v1555 = _bittest(&v20, a8);
  v21 = 294913;
  v1564 = _bittest(&v21, a8);
  v22 = 327681;
  v1566 = _bittest(&v22, a8);
  v23 = 262147;
  v1567 = _bittest(&v23, a8);
  v24 = 278529;
  v1569 = _bittest(&v24, a8);
  v25 = 262149;
  v1573 = _bittest(&v25, a8);
  v26 = 263169;
  v1561 = _bittest(&v26, a8);
  v27 = 270337;
  v28 = _bittest(&v27, a8);
  v29 = 262401;
  v1562 = v28;
  v28 = _bittest(&v29, a8);
  v30 = 262153;
  v1563 = v28;
  v1565 = _bittest(&v30, a8);
  v31 = a7 ^ 1;
  LODWORD(v32) = a5;
  v33 = a9;
  v1603 = a1;
  LOBYTE(v1604) = (unsigned __int8)a8 < 0x13u;
  if ( (a6 | a5) != 1 )
    goto LABEL_89;
  if ( v31 == 0 )
    goto LABEL_89;
  v34 = a9 & v10 & v13;
  v35 = a9 & v10 & v15;
  if ( (v35 | v34) == 0 )
    goto LABEL_89;
  v1605 = a7 ^ 1;
  sub_14121A480(a1: &v1579);
  if ( v35 == 0 )
    goto LABEL_42;
  v36 = *((_DWORD *)a1 + 92);
  sub_14080D0E0(a1: &v1583, a2: 0x1418E2C24LL);
  LODWORD(v1585) = v36;
  v1594 = v36;
  v1586 = 9;
  sub_1408085A0(a1: &v1600, a2: &v1586);
  sub_1408085A0(a1: &v1596, a2: &v1594);
  v1602 = nullptr;
  v37 = (int *)v1596;
  if ( v1596 != nullptr )
  {
    _InterlockedIncrement(v1596 - 1);
    v1602 = v37;
    v38 = *v37;
  }
  else
  {
    v38 = 0;
  }
  v39 = v38 + 1;
  v40 = sub_1412EC810(a1: 264, a2: (unsigned int)(v38 + 1));
  v41 = (volatile signed __int32 *)v40;
  *(_DWORD *)v40 = 0;
  v42 = 0;
  if ( v38 + 1 <= 0 )
    v39 = 0;
  *(_DWORD *)(v40 + 4) = v39;
  v43 = v40 + 8;
  *(_BYTE *)(v40 + 8) = 0;
  if ( v38 <= 0 )
  {
    v45 = (_BYTE *)(v40 + 8);
    if ( v38 != 0 )
      goto LABEL_16;
  }
  else
  {
    v44 = 0x1419435F1LL;
    if ( v1602 != nullptr )
      v44 = (__int64)(v1602 + 1);
    sub_141758A00(a1: v40 + 8, a2: v44, a3: (unsigned int)v38);
    v45 = (_BYTE *)(v43 + (unsigned int)v38);
  }
  *v45 = 0;
  v42 = v38;
LABEL_16:
  v46 = v40 + 4;
  *(_WORD *)(v43 + v42) = 95;
  v47 = v1602 - 1;
  if ( v1602 != nullptr && _InterlockedDecrement(v47) == 0 )
    sub_1412EC9A0(a1: v47);
  v1602 = nullptr;
  _InterlockedIncrement(v41);
  v1602 = (volatile signed __int32 *)v46;
  sub_140809550(a1: &v1602, a2: v1587, a3: &v1600);
  v1593 = 0;
  v48 = v1587[0];
  v49 = v1603;
  if ( v1587[0] != 0 )
  {
    _InterlockedIncrement((volatile signed __int32 *)(v1587[0] - 4LL));
    v50 = v1587[0];
    v1593 = v48;
    if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] - 4LL)) == 0 )
      sub_1412EC9A0(a1: v50 - 4);
  }
  v51 = v1602;
  if ( v1602 != nullptr && _InterlockedDecrement(v1602 - 1) == 0 )
    sub_1412EC9A0(a1: v51 - 1);
  v52 = v1596;
  if ( v1596 != nullptr && _InterlockedDecrement(v1596 - 1) == 0 )
    sub_1412EC9A0(a1: v52 - 1);
  v53 = v1600;
  if ( v1600 != nullptr && _InterlockedDecrement(v1600 - 1) == 0 )
    sub_1412EC9A0(a1: v53 - 1);
  v1587[0] = 0x80100004E554C4CLL;
  sub_1407D0F70(
    a1: (unsigned int)v1587,
    a2: (unsigned int)&v1595,
    a3: a2,
    a4: (unsigned int)&v1593,
    a5: (__int64)&v1583,
    a6: 0,
    a7: 0,
    0);
  v54 = v1593;
  if ( v1593 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1593 - 4)) == 0 )
    sub_1412EC9A0(a1: v54 - 4);
  v55 = v1595;
  LODWORD(v32) = a5;
  if ( v1595 == nullptr )
    goto LABEL_2928;
  v56 = v49[22] != v49[21];
  LODWORD(v1602) = 0;
  (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **, __int64))(*(_QWORD *)v1595 + 40LL))(
    a1: v1595,
    a2: &v1602,
    a3: 4);
  if ( *((_DWORD *)v55 + 4) != 0 )
    goto LABEL_37;
  if ( v1601 != 0 )
  {
    LOBYTE(v57) = 1;
    if ( (int)v1602 <= 0 )
      goto LABEL_38;
    v117 = 0;
    while ( 1 )
    {
      memset(v1587, 0, sizeof(v1587));
      *(_QWORD *)&v1588 = 0;
      WORD6(v1588) = -1;
      DWORD2(v1588) = 0;
      v1600 = v1595;
      if ( v1595 != nullptr )
        _InterlockedIncrement(v1595 + 2);
      v118 = sub_1410706E0(a1: v1587, a2: &v1600, a3: (unsigned int)v1585);
      v119 = v1600;
      if ( v1600 != nullptr && _InterlockedDecrement(v1600 + 2) == 0 )
        (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v119)(a1: v119, a2: 1);
      if ( v118 == 0 )
        break;
      sub_14106FF40(a1: v1587);
      sub_140E44A40(a1: &v1588);
      v120 = v1587[3];
      if ( v1587[3] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[3] - 4LL)) == 0 )
        sub_1412EC9A0(a1: v120 - 4);
      v121 = v1587[2];
      if ( v1587[2] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[2] - 4LL)) == 0 )
        sub_1412EC9A0(a1: v121 - 4);
      v122 = v1587[1];
      if ( v1587[1] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[1] - 4LL)) == 0 )
        sub_1412EC9A0(a1: v122 - 4);
      v123 = v1587[0];
      if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] - 4LL)) == 0 )
        sub_1412EC9A0(a1: v123 - 4);
      if ( ++v117 >= (int)v1602 )
      {
        LODWORD(v32) = a5;
        LOBYTE(v57) = 1;
        goto LABEL_38;
      }
    }
    sub_140E44A40(a1: &v1588);
    v435 = v1587[3];
    if ( v1587[3] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[3] - 4LL)) == 0 )
      sub_1412EC9A0(a1: v435 - 4);
    v436 = v1587[2];
    LODWORD(v32) = a5;
    if ( v1587[2] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[2] - 4LL)) == 0 )
      sub_1412EC9A0(a1: v436 - 4);
    v437 = v1587[1];
    if ( v1587[1] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[1] - 4LL)) == 0 )
      sub_1412EC9A0(a1: v437 - 4);
    v438 = v1587[0];
    if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] - 4LL)) == 0 )
      sub_1412EC9A0(a1: v438 - 4);
LABEL_37:
    LOBYTE(v57) = 0;
    goto LABEL_38;
  }
  v184 = (int)v1602;
  v185 = v56;
  if ( v56 )
  {
    v186 = v1603[21];
    v187 = (v1603[22] - v186) >> 3;
    v188 = v187 + (int)v1602;
    v189 = (v1603[23] - v186) >> 3;
    if ( v189 < v188 )
    {
      if ( v188 >> 61 == 0 )
      {
        v190 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v188);
        v191 = v1603;
        sub_141758A00(a1: v190, a2: v1603[21], a3: v1603[22] - v1603[21]);
        if ( v191[21] != 0 )
          sub_1407E4890(a1: qword_141ABD470);
        v191[21] = v190;
        v191[22] = v190 + 8 * v187;
        v192 = v190 + 8 * v188;
LABEL_511:
        v191[23] = v192;
        goto LABEL_512;
      }
      goto LABEL_3113;
    }
  }
  else
  {
    v312 = v1603[21];
    v189 = (v1603[23] - v312) >> 3;
    if ( v189 < (int)v1602 )
    {
      if ( (int)v1602 >= 0 )
      {
        v191 = v1603;
        v313 = v1603[22];
        v314 = sub_1407E4490(a1: qword_141ABD470, a2: 8LL * (int)v1602);
        sub_141758A00(a1: v314, a2: v191[21], a3: v191[22] - v191[21]);
        if ( v191[21] != 0 )
          sub_1407E4890(a1: qword_141ABD470);
        v191[21] = v314;
        v191[22] = v314 + v313 - v312;
        v192 = v314 + 8 * v184;
        goto LABEL_511;
      }
LABEL_3113:
      sub_1400526C0(a1: v189);
    }
  }
LABEL_512:
  if ( (int)v1602 <= 0 )
  {
    LOBYTE(v57) = 1;
    LODWORD(v32) = a5;
    goto LABEL_38;
  }
  LODWORD(v32) = a5;
  if ( !v185 )
  {
    v445 = 0;
    v1557 = v34;
    do
    {
      if ( dword_141B60970 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(a1: &dword_141B60970);
        if ( dword_141B60970 == -1 )
        {
          sub_1407E53D0(
            a1: (unsigned int)&unk_141B60920,
            a2: 1100150639,
            a3: 1024,
            a4: 48,
            a5: 0,
            a6: 1,
            a7: 1024,
            a8: 4096);
          sub_141751048(a1: sub_140FE1840);
          sub_141750EA0(a1: &dword_141B60970);
        }
      }
      v446 = sub_1407E58C0(a1: &unk_141B60920, a2: 48);
      *(_QWORD *)v446 = 0;
      *(_QWORD *)(v446 + 8) = 0;
      *(_QWORD *)(v446 + 16) = 0;
      *(_QWORD *)(v446 + 24) = 0;
      *(_QWORD *)(v446 + 32) = 0;
      *(_WORD *)(v446 + 44) = -1;
      *(_DWORD *)(v446 + 40) = 0;
      v1587[0] = v1595;
      if ( v1595 != nullptr )
        _InterlockedIncrement(v1595 + 2);
      LODWORD(v57) = sub_1410706E0(a1: v446, a2: v1587, a3: (unsigned int)v1585);
      v447 = (void (__fastcall ***)(_QWORD, __int64))v1587[0];
      if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] + 8LL)) == 0 )
        (**v447)(a1: v447, a2: 1);
      if ( (_BYTE)v57 == 0 )
        break;
      v448 = v1603;
      v449 = (__int64 *)v1603[22];
      if ( v449 == (__int64 *)v1603[23] )
      {
        LODWORD(v1582) = v57;
        v450 = (__int64)v449 - v1603[21];
        v451 = v450 >> 3;
        v452 = (unsigned __int64)(v450 >> 3) >> 1;
        v453 = 0x1FFFFFFFFFFFFFFFLL - v452;
        v32 = (v450 >> 3) + v452;
        v1576 = (v450 >> 3) + 1;
        if ( v32 <= v1576 )
          v32 = v451 + 1;
        if ( v451 > v453 )
          v32 = 0x1FFFFFFFFFFFFFFFLL;
        v57 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v32);
        *(_QWORD *)(v57 + v450) = v446;
        v454 = (__int64 *)v448[22];
        sub_141758A00(a1: v57, a2: v448[21], a3: (char *)v449 - v448[21]);
        if ( v454 != v449 )
          sub_141758A00(a1: v57 + v450 + 8, a2: v449, a3: v448[22] - (_QWORD)v449);
        v455 = v448[21];
        v34 = v1557;
        if ( v455 != 0 )
        {
          v456 = v448[23] - v455;
          if ( v456 == -1 )
            v456 = *(unsigned int *)(v455 - *(unsigned int *)(qword_141ABD470 + 48));
          if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
            && (v457 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v457) >> 3 > v456)
            && (v458 = *(_QWORD *)(v457 + 8 * v456)) != 0 )
          {
            MEMORY[0x1419475D8](a1: v458 + 32, a2: v455 - *(unsigned int *)(v458 + 120));
            v459 = *(_BYTE *)(v458 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v458 + 64)) != 0;
            v448 = v1603;
            if ( !v459 && *(_BYTE *)(v458 + 97) != 0 )
              sub_1412D33C0(a1: v458);
          }
          else
          {
            MEMORY[0x141948990](a1: v455 - *(unsigned int *)(qword_141ABD470 + 48));
            v448 = v1603;
          }
        }
        v448[21] = v57;
        v448[22] = v57 + 8 * v1576;
        v448[23] = v57 + 8 * v32;
        LODWORD(v32) = a5;
        LOBYTE(v57) = v1582;
      }
      else
      {
        *v449 = v446;
        v448[22] += 8LL;
      }
      ++v445;
    }
    while ( v445 < (int)v1602 );
    goto LABEL_38;
  }
  v315 = 0;
  while ( 1 )
  {
    if ( dword_141B60970 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(a1: &dword_141B60970);
      if ( dword_141B60970 == -1 )
      {
        sub_1407E53D0(
          a1: (unsigned int)&unk_141B60920,
          a2: 1100150639,
          a3: 1024,
          a4: 48,
          a5: 0,
          a6: 1,
          a7: 1024,
          a8: 4096);
        sub_141751048(a1: sub_140FE1840);
        sub_141750EA0(a1: &dword_141B60970);
      }
    }
    v341 = sub_1407E58C0(a1: &unk_141B60920, a2: 48);
    *(_QWORD *)v341 = 0;
    *(_QWORD *)(v341 + 8) = 0;
    *(_QWORD *)(v341 + 16) = 0;
    *(_QWORD *)(v341 + 24) = 0;
    *(_QWORD *)(v341 + 32) = 0;
    *(_WORD *)(v341 + 44) = -1;
    *(_DWORD *)(v341 + 40) = 0;
    v1587[0] = v1595;
    if ( v1595 != nullptr )
      _InterlockedIncrement(v1595 + 2);
    v342 = sub_1410706E0(a1: v341, a2: v1587, a3: (unsigned int)v1585);
    v343 = (void (__fastcall ***)(_QWORD, __int64))v1587[0];
    if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] + 8LL)) == 0 )
      (**v343)(a1: v343, a2: 1);
    if ( (_BYTE)v342 == 0 )
      break;
    v1575 = v315;
    LODWORD(v1582) = v342;
    v344 = v1603[21];
    v345 = (__int64 *)v1603[22];
    v346 = (__int64)v345 - v344;
    v347 = (__int64 *)v344;
    if ( (__int64)v345 - v344 > 0 )
    {
      v348 = (unsigned __int64)v346 >> 3;
      v347 = (__int64 *)v1603[21];
      v349 = (unsigned __int64)v346 >> 3;
      do
      {
        v349 = (unsigned __int64)v349 >> 1;
        if ( *(_DWORD *)(v347[v349] + 40) < *(_DWORD *)(v341 + 40) )
        {
          v347 += v349 + 1;
          v349 = v348 + ~v349;
        }
        v348 = v349;
      }
      while ( v349 > 0 );
    }
    if ( v347 == v345 )
    {
      v369 = v1603;
      if ( v345 == (__int64 *)v1603[23] )
      {
        v372 = (unsigned __int64)(v346 >> 3) >> 1;
        v373 = 0x1FFFFFFFFFFFFFFFLL - v372;
        v374 = (v346 >> 3) + v372;
        v1559 = (v346 >> 3) + 1;
        if ( v374 <= v1559 )
          v374 = (v346 >> 3) + 1;
        if ( v346 >> 3 > v373 )
          v374 = 0x1FFFFFFFFFFFFFFFLL;
        v1554 = v374;
        v375 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v374);
        *(_QWORD *)(v375 + v346) = v341;
        v376 = (__int64 *)v369[22];
        sub_141758A00(a1: v375, a2: v369[21], a3: (char *)v345 - v369[21]);
        v377 = v369;
        if ( v376 != v345 )
          sub_141758A00(a1: v375 + v346 + 8, a2: v345, a3: v369[22] - (_QWORD)v345);
        v378 = v369[21];
        LODWORD(v32) = a5;
        v340 = v1575;
        v379 = v375;
        if ( v378 != 0 )
        {
          v380 = v369[23] - v378;
          if ( v380 == -1 )
            v380 = *(unsigned int *)(v378 - *(unsigned int *)(qword_141ABD470 + 48));
          if ( *(_BYTE *)(qword_141ABD470 + 52) == 0
            || (v381 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v381) >> 3 <= v380)
            || (v382 = *(_QWORD *)(v381 + 8 * v380)) == 0 )
          {
            MEMORY[0x141948990](a1: v378 - *(unsigned int *)(qword_141ABD470 + 48));
            goto LABEL_662;
          }
          MEMORY[0x1419475D8](a1: v382 + 32, a2: v378 - *(unsigned int *)(v382 + 120));
          v383 = *(_BYTE *)(v382 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v382 + 64)) != 0;
          v379 = v375;
          if ( !v383 && *(_BYTE *)(v382 + 97) != 0 )
          {
            sub_1412D33C0(a1: v382);
LABEL_662:
            v379 = v375;
          }
        }
        v377[21] = v379;
        v377[22] = v379 + 8 * v1559;
        v377[23] = v379 + 8 * v1554;
LABEL_666:
        LOBYTE(v57) = v1582;
        goto LABEL_580;
      }
      *v345 = v341;
      v369[22] += 8LL;
    }
    else
    {
      v350 = ((__int64)v347 - v344) >> 3;
      if ( *(_DWORD *)(*v347 + 40) == *(_DWORD *)(v341 + 40) )
      {
        v351 = v346 >> 3;
        if ( v351 > v350 )
        {
          v352 = *(__int64 **)(v344 + 8 * v350);
          if ( v352 != nullptr )
          {
            sub_140E44A40(a1: v352 + 4);
            v353 = v352[3];
            if ( v353 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v353 - 4)) == 0 )
              sub_1412EC9A0(a1: v353 - 4);
            v354 = v352[2];
            if ( v354 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v354 - 4)) == 0 )
              sub_1412EC9A0(a1: v354 - 4);
            v355 = v352[1];
            if ( v355 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v355 - 4)) == 0 )
              sub_1412EC9A0(a1: v355 - 4);
            v356 = *v352;
            if ( *v352 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v356 - 4)) == 0 )
              sub_1412EC9A0(a1: v356 - 4);
            sub_140FE16E0(a1: v352);
            v344 = v1603[21];
            v345 = (__int64 *)v1603[22];
            v351 = ((__int64)v345 - v344) >> 3;
          }
        }
        if ( v351 <= v350 )
        {
          v357 = v350 + 1;
          v358 = v350 + 1 - v351;
          if ( v350 + 1 < v351 )
          {
            v1603[22] = v344 + 8 * v357;
          }
          else if ( v350 + 1 > v351 )
          {
            v359 = (v1603[23] - v344) >> 3;
            if ( v359 >= v357 )
            {
              v397 = &v345[v358];
              v398 = v1603;
              sub_141758A10(a1: v345, a2: 0, a3: 8 * v358);
              v398[22] = v397;
              v344 = v398[21];
            }
            else
            {
              v189 = v357 >> 61;
              if ( v357 >> 61 != 0 )
                goto LABEL_3113;
              v360 = v359 + (v359 >> 1);
              if ( v360 <= v357 )
                v360 = v350 + 1;
              if ( v359 > 0x1FFFFFFFFFFFFFFFLL - (v359 >> 1) )
                v360 = 0x1FFFFFFFFFFFFFFFLL;
              v344 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v360);
              sub_141758A10(a1: v344 + 8 * v351, a2: 0, a3: 8 * (v350 + 1 - v351));
              v361 = v1603;
              sub_141758A00(a1: v344, a2: v1603[21], a3: v1603[22] - v1603[21]);
              v362 = v361[21];
              if ( v362 != 0 )
              {
                v363 = v361[23] - v362;
                if ( v363 == -1 )
                  v363 = *(unsigned int *)(v362 - *(unsigned int *)(qword_141ABD470 + 48));
                if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                  && (v364 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v364) >> 3 > v363)
                  && (v365 = *(_QWORD *)(v364 + 8 * v363)) != 0 )
                {
                  v366 = v365;
                  MEMORY[0x1419475D8](a1: v365 + 32, a2: v362 - *(unsigned int *)(v365 + 120));
                  v367 = v366;
                  v368 = *(_BYTE *)(v366 + 72) != 0
                      && _InterlockedDecrement((volatile signed __int32 *)(v366 + 64)) != 0;
                  v361 = v1603;
                  if ( !v368 && *(_BYTE *)(v367 + 97) != 0 )
                    sub_1412D33C0(a1: v367);
                }
                else
                {
                  MEMORY[0x141948990](a1: v362 - *(unsigned int *)(qword_141ABD470 + 48));
                  v361 = v1603;
                }
              }
              v361[21] = v344;
              v361[22] = v344 + 8 * (v350 + 1);
              v361[23] = v344 + 8 * v360;
            }
          }
        }
        *(_QWORD *)(v344 + 8 * v350) = v341;
      }
      else
      {
        v370 = (__int64 *)(v344 + 8 * v350);
        v371 = v1603;
        if ( v345 == (__int64 *)v1603[23] )
        {
          v384 = v346 >> 3;
          v385 = v350;
          v386 = v384 + (v384 >> 1);
          v1560 = v384 + 1;
          if ( v386 <= v384 + 1 )
            v386 = v384 + 1;
          v387 = v386;
          v388 = v385;
          if ( v384 > 0x1FFFFFFFFFFFFFFFLL - (v384 >> 1) )
            v387 = 0x1FFFFFFFFFFFFFFFLL;
          v32 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v387);
          *(_QWORD *)(v32 + 8 * v388) = v341;
          v389 = (__int64 *)v371[22];
          sub_141758A00(a1: v32, a2: v371[21], a3: (char *)v370 - v371[21]);
          v390 = v389 == v370;
          v391 = v371;
          if ( !v390 )
            sub_141758A00(a1: v32 + 8 * v388 + 8, a2: v370, a3: v371[22] - (_QWORD)v370);
          v392 = v371[21];
          v340 = v1575;
          if ( v392 != 0 )
          {
            v393 = v371[23] - v392;
            if ( v393 == -1 )
              v393 = *(unsigned int *)(v392 - *(unsigned int *)(qword_141ABD470 + 48));
            if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
              && (v394 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v394) >> 3 > v393)
              && (v395 = *(_QWORD *)(v394 + 8 * v393)) != 0 )
            {
              MEMORY[0x1419475D8](a1: v395 + 32, a2: v392 - *(unsigned int *)(v395 + 120));
              v396 = *(_BYTE *)(v395 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v395 + 64)) != 0;
              if ( !v396 && *(_BYTE *)(v395 + 97) != 0 )
                sub_1412D33C0(a1: v395);
            }
            else
            {
              MEMORY[0x141948990](a1: v392 - *(unsigned int *)(qword_141ABD470 + 48));
            }
          }
          v391[21] = v32;
          v391[22] = v32 + 8 * v1560;
          v391[23] = v32 + 8 * v387;
          LODWORD(v32) = a5;
          goto LABEL_666;
        }
        if ( v345 == v370 )
        {
          *v345 = v341;
          v1603[22] += 8LL;
        }
        else
        {
          *v345 = *(v345 - 1);
          v1603[22] += 8LL;
          sub_141758A00(a1: v370 + 1, a2: v370, a3: (char *)(v345 - 1) - (char *)v370);
          *v370 = v341;
        }
      }
    }
    LODWORD(v32) = a5;
    LOBYTE(v57) = v1582;
    v340 = v1575;
LABEL_580:
    v315 = v340 + 1;
    if ( v315 >= (int)v1602 )
      goto LABEL_38;
  }
  LOBYTE(v57) = 0;
  LODWORD(v32) = a5;
LABEL_38:
  v58 = v1595;
  if ( v1595 != nullptr && _InterlockedDecrement(v1595 + 2) == 0 )
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v58)(a1: v58, a2: 1);
  a1 = v1603;
  LODWORD(v10) = (unsigned __int8)v1604;
  if ( (_BYTE)v57 == 0 )
    goto LABEL_2928;
LABEL_42:
  v59 = qword_141B59FA0;
  if ( qword_141B59FA0 != 0 && v1581 != 0 )
  {
    v60 = v1580;
    v61 = (unsigned int)MEMORY[0x141947498]();
    v62 = *(_QWORD *)(v59 + 16);
    if ( v62 == 0 || v62 == (unsigned int)v61 )
    {
      if ( v60 == 0 )
        v61 = 0;
      *(_QWORD *)(v59 + 16) = v61;
    }
    *(_QWORD *)(v59 + 8) = v1579;
  }
  v33 = a9;
  v31 = v1605;
  if ( v34 == 0 )
    goto LABEL_89;
  v63 = *((_DWORD *)a1 + 92);
  sub_14080D0E0(a1: &v1595, a2: 0x1418E2C24LL);
  LODWORD(v1585) = v63;
  LODWORD(v1593) = v63;
  v1594 = 3;
  sub_1408085A0(a1: &v1579, a2: &v1594);
  sub_1408085A0(a1: &v1602, a2: &v1593);
  v1600 = nullptr;
  v64 = v1602;
  if ( v1602 != nullptr )
  {
    _InterlockedIncrement(v1602 - 1);
    v1600 = v64;
    v65 = *v64;
  }
  else
  {
    v65 = 0;
  }
  v66 = v65 + 1;
  v67 = sub_1412EC810(a1: 264, a2: (unsigned int)(v65 + 1));
  v68 = (volatile signed __int32 *)v67;
  *(_DWORD *)v67 = 0;
  v69 = 0;
  if ( v65 + 1 <= 0 )
    v66 = 0;
  *(_DWORD *)(v67 + 4) = v66;
  v70 = v67 + 8;
  *(_BYTE *)(v67 + 8) = 0;
  if ( v65 <= 0 )
  {
    v72 = (_BYTE *)(v67 + 8);
    if ( v65 == 0 )
      goto LABEL_60;
  }
  else
  {
    v71 = 0x1419435F1LL;
    if ( v1600 != nullptr )
      v71 = (__int64)(v1600 + 1);
    sub_141758A00(a1: v67 + 8, a2: v71, a3: (unsigned int)v65);
    v72 = (_BYTE *)(v70 + (unsigned int)v65);
LABEL_60:
    *v72 = 0;
    v69 = v65;
  }
  v73 = (volatile signed __int32 *)(v67 + 4);
  *(_WORD *)(v70 + v69) = 95;
  v74 = v1600 - 1;
  if ( v1600 != nullptr && _InterlockedDecrement(v74) == 0 )
    sub_1412EC9A0(a1: v74);
  v1600 = nullptr;
  _InterlockedIncrement(v68);
  v1600 = v73;
  sub_140809550(a1: &v1600, a2: v1587, a3: &v1579);
  v1583 = 0;
  v75 = v1587[0];
  if ( v1587[0] != 0 )
  {
    _InterlockedIncrement((volatile signed __int32 *)(v1587[0] - 4LL));
    v76 = v1587[0];
    v1583 = v75;
    if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] - 4LL)) == 0 )
      sub_1412EC9A0(a1: v76 - 4);
  }
  v77 = v1600;
  LODWORD(v32) = a5;
  if ( v1600 != nullptr && _InterlockedDecrement(v1600 - 1) == 0 )
    sub_1412EC9A0(a1: v77 - 1);
  v78 = v1602;
  if ( v1602 != nullptr && _InterlockedDecrement(v1602 - 1) == 0 )
    sub_1412EC9A0(a1: v78 - 1);
  v79 = v1579;
  if ( v1579 != nullptr && _InterlockedDecrement(v1579 - 1) == 0 )
    sub_1412EC9A0(a1: v79 - 1);
  v1587[0] = 0x80100004E554C4CLL;
  LOBYTE(v1553) = 0;
  sub_1407D0F70(
    a1: (unsigned int)v1587,
    a2: (unsigned int)&v1596,
    a3: a2,
    a4: (unsigned int)&v1583,
    a5: (__int64)&v1595,
    a6: 0,
    a7: 0,
    v1553);
  v80 = v1583;
  if ( v1583 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1583 - 4)) == 0 )
    sub_1412EC9A0(a1: v80 - 4);
  v81 = v1596;
  if ( v1596 == nullptr )
    goto LABEL_2936;
  v82 = a1[7] != a1[6];
  LODWORD(v1600) = 0;
  (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **, __int64))(*(_QWORD *)v1596 + 40LL))(
    a1: v1596,
    a2: &v1600,
    a3: 4);
  if ( *((_DWORD *)v81 + 4) != 0 )
  {
    LOBYTE(v83) = 0;
    LODWORD(v10) = (unsigned __int8)v1604;
LABEL_84:
    v31 = v1605;
    goto LABEL_85;
  }
  LODWORD(v10) = (unsigned __int8)v1604;
  if ( v1601 != 0 )
  {
    LOBYTE(v83) = 1;
    if ( (int)v1600 > 0 )
    {
      v153 = 0;
      while ( 1 )
      {
        v1588 = 0;
        memset(v1587, 0, sizeof(v1587));
        v1589 = 0;
        v1592 = -1;
        v1591 = -1;
        v1590 = 0;
        v1579 = v1596;
        if ( v1596 != nullptr )
          _InterlockedIncrement(v1596 + 2);
        v154 = sub_140E78C10(a1: v1587, a2: &v1579, a3: (unsigned int)v1585);
        v155 = v1579;
        if ( v1579 != nullptr && _InterlockedDecrement(v1579 + 2) == 0 )
          (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v155)(a1: v155, a2: 1);
        if ( v154 == 0 )
          break;
        sub_140E78080(a1: v1587);
        sub_140E44A40(a1: &v1589);
        v156 = *((_QWORD *)&v1588 + 1);
        if ( *((_QWORD *)&v1588 + 1) != 0
          && _InterlockedDecrement((volatile signed __int32 *)(*((_QWORD *)&v1588 + 1) - 4LL)) == 0 )
        {
          sub_1412EC9A0(a1: v156 - 4);
        }
        v157 = v1588;
        if ( (_QWORD)v1588 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1588 - 4)) == 0 )
          sub_1412EC9A0(a1: v157 - 4);
        v158 = v1587[3];
        if ( v1587[3] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[3] - 4LL)) == 0 )
          sub_1412EC9A0(a1: v158 - 4);
        v159 = v1587[2];
        if ( v1587[2] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[2] - 4LL)) == 0 )
          sub_1412EC9A0(a1: v159 - 4);
        v160 = v1587[1];
        if ( v1587[1] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[1] - 4LL)) == 0 )
          sub_1412EC9A0(a1: v160 - 4);
        v161 = v1587[0];
        if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] - 4LL)) == 0 )
          sub_1412EC9A0(a1: v161 - 4);
        if ( ++v153 >= (int)v1600 )
        {
          v31 = v1605;
          LODWORD(v32) = a5;
          LOBYTE(v83) = 1;
          goto LABEL_85;
        }
      }
      sub_140E44A40(a1: &v1589);
      v640 = *((_QWORD *)&v1588 + 1);
      if ( *((_QWORD *)&v1588 + 1) != 0
        && _InterlockedDecrement((volatile signed __int32 *)(*((_QWORD *)&v1588 + 1) - 4LL)) == 0 )
      {
        sub_1412EC9A0(a1: v640 - 4);
      }
      v641 = v1588;
      LODWORD(v32) = a5;
      if ( (_QWORD)v1588 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1588 - 4)) == 0 )
        sub_1412EC9A0(a1: v641 - 4);
      v642 = v1587[3];
      if ( v1587[3] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[3] - 4LL)) == 0 )
        sub_1412EC9A0(a1: v642 - 4);
      v643 = v1587[2];
      if ( v1587[2] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[2] - 4LL)) == 0 )
        sub_1412EC9A0(a1: v643 - 4);
      v644 = v1587[1];
      if ( v1587[1] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[1] - 4LL)) == 0 )
        sub_1412EC9A0(a1: v644 - 4);
      v645 = v1587[0];
      if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] - 4LL)) == 0 )
        sub_1412EC9A0(a1: v645 - 4);
      LOBYTE(v83) = 0;
    }
    goto LABEL_84;
  }
  v258 = (int)v1600;
  v259 = v82;
  if ( v82 )
  {
    v260 = a1[6];
    v261 = (a1[7] - v260) >> 3;
    v262 = v261 + (int)v1600;
    v263 = (a1[8] - v260) >> 3;
    v31 = v1605;
    if ( v263 < v262 )
    {
      if ( v262 >> 61 == 0 )
      {
        v264 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v262);
        sub_141758A00(a1: v264, a2: a1[6], a3: a1[7] - a1[6]);
        if ( a1[6] != 0 )
          sub_1407E4890(a1: qword_141ABD470);
        a1[6] = v264;
        a1[7] = v264 + 8 * v261;
        a1[8] = v264 + 8 * v262;
        goto LABEL_743;
      }
LABEL_3115:
      sub_1400526C0(a1: v263);
    }
  }
  else
  {
    v430 = a1[6];
    v263 = (a1[8] - v430) >> 3;
    v31 = v1605;
    if ( v263 < (int)v1600 )
    {
      if ( (int)v1600 < 0 )
        goto LABEL_3115;
      v431 = a1[7];
      v432 = a1;
      v433 = sub_1407E4490(a1: qword_141ABD470, a2: 8LL * (int)v1600);
      sub_141758A00(a1: v433, a2: v432[6], a3: v432[7] - v432[6]);
      if ( v432[6] != 0 )
        sub_1407E4890(a1: qword_141ABD470);
      v432[6] = v433;
      v432[7] = v433 + v431 - v430;
      v432[8] = v433 + 8 * v258;
      a1 = v432;
LABEL_743:
      v31 = v1605;
    }
  }
  if ( (int)v1600 <= 0 )
  {
    LOBYTE(v83) = 1;
    LODWORD(v32) = a5;
    goto LABEL_85;
  }
  LODWORD(v32) = a5;
  if ( !v259 )
  {
    v653 = 0;
    while ( 1 )
    {
      if ( dword_141B60B28 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(a1: &dword_141B60B28);
        if ( dword_141B60B28 == -1 )
        {
          sub_1407E53D0(
            a1: (unsigned int)&unk_141B60AD8,
            a2: 1100150726,
            a3: 2048,
            a4: 72,
            a5: 0,
            a6: 1,
            a7: 2048,
            a8: 4096);
          sub_141751048(a1: sub_140FE1F70);
          sub_141750EA0(a1: &dword_141B60B28);
        }
      }
      v654 = sub_1407E58C0(a1: &unk_141B60AD8, a2: 72);
      *(_QWORD *)v654 = 0;
      *(_QWORD *)(v654 + 8) = 0;
      *(_QWORD *)(v654 + 16) = 0;
      *(_QWORD *)(v654 + 24) = 0;
      *(_QWORD *)(v654 + 32) = 0;
      *(_QWORD *)(v654 + 40) = 0;
      *(_QWORD *)(v654 + 48) = 0;
      *(_BYTE *)(v654 + 64) = -1;
      *(_QWORD *)(v654 + 56) = 0xFFFFFFFF00000000uLL;
      v1587[0] = v1596;
      if ( v1596 != nullptr )
        _InterlockedIncrement(v1596 + 2);
      v83 = sub_140E78C10(a1: v654, a2: v1587, a3: (unsigned int)v1585);
      v655 = (void (__fastcall ***)(_QWORD, __int64))v1587[0];
      if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] + 8LL)) == 0 )
        (**v655)(a1: v655, a2: 1);
      if ( (_BYTE)v83 == 0 )
        goto LABEL_84;
      v656 = (__int64 *)a1[7];
      v31 = v1605;
      if ( v656 == (__int64 *)a1[8] )
      {
        LODWORD(v1582) = v83;
        v657 = (__int64)v656 - a1[6];
        v658 = v657 >> 3;
        v10 = (__int64)a1;
        v659 = (unsigned __int64)(v657 >> 3) >> 1;
        v660 = 0x1FFFFFFFFFFFFFFFLL - v659;
        v661 = (v657 >> 3) + v659;
        v1558 = (v657 >> 3) + 1;
        if ( v661 <= v1558 )
          v661 = v658 + 1;
        if ( v658 > v660 )
          v661 = 0x1FFFFFFFFFFFFFFFLL;
        v32 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v661);
        *(_QWORD *)(v32 + v657) = v654;
        v662 = *(__int64 **)(v10 + 56);
        sub_141758A00(a1: v32, a2: *(_QWORD *)(v10 + 48), a3: (char *)v656 - *(_QWORD *)(v10 + 48));
        if ( v662 != v656 )
          sub_141758A00(a1: v32 + v657 + 8, a2: v656, a3: *(_QWORD *)(v10 + 56) - (_QWORD)v656);
        v663 = *(_QWORD *)(v10 + 48);
        LOBYTE(v83) = v1582;
        if ( v663 != 0 )
        {
          v664 = *(_QWORD *)(v10 + 64) - v663;
          if ( v664 == -1 )
            v664 = *(unsigned int *)(v663 - *(unsigned int *)(qword_141ABD470 + 48));
          if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
            && (v665 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v665) >> 3 > v664)
            && (v666 = *(_QWORD *)(v665 + 8 * v664)) != 0 )
          {
            MEMORY[0x1419475D8](a1: v666 + 32, a2: v663 - *(unsigned int *)(v666 + 120));
            v667 = *(_BYTE *)(v666 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v666 + 64)) != 0;
            v10 = (__int64)v1603;
            if ( !v667 && *(_BYTE *)(v666 + 97) != 0 )
              sub_1412D33C0(a1: v666);
          }
          else
          {
            MEMORY[0x141948990](a1: v663 - *(unsigned int *)(qword_141ABD470 + 48));
            v10 = (__int64)v1603;
          }
        }
        *(_QWORD *)(v10 + 48) = v32;
        *(_QWORD *)(v10 + 56) = v32 + 8 * v1558;
        *(_QWORD *)(v10 + 64) = v32 + 8 * v661;
        a1 = (_QWORD *)v10;
        LODWORD(v10) = (unsigned __int8)v1604;
        v31 = v1605;
        LODWORD(v32) = a5;
      }
      else
      {
        *v656 = v654;
        a1[7] += 8LL;
      }
      if ( ++v653 >= (int)v1600 )
        goto LABEL_85;
    }
  }
  v434 = 0;
  while ( 2 )
  {
    if ( dword_141B60B28 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(a1: &dword_141B60B28);
      if ( dword_141B60B28 == -1 )
      {
        sub_1407E53D0(
          a1: (unsigned int)&unk_141B60AD8,
          a2: 1100150726,
          a3: 2048,
          a4: 72,
          a5: 0,
          a6: 1,
          a7: 2048,
          a8: 4096);
        sub_141751048(a1: sub_140FE1F70);
        sub_141750EA0(a1: &dword_141B60B28);
      }
    }
    v535 = sub_1407E58C0(a1: &unk_141B60AD8, a2: 72);
    *(_QWORD *)v535 = 0;
    *(_QWORD *)(v535 + 8) = 0;
    *(_QWORD *)(v535 + 16) = 0;
    *(_QWORD *)(v535 + 24) = 0;
    *(_QWORD *)(v535 + 32) = 0;
    *(_QWORD *)(v535 + 40) = 0;
    *(_QWORD *)(v535 + 48) = 0;
    *(_BYTE *)(v535 + 64) = -1;
    *(_QWORD *)(v535 + 56) = 0xFFFFFFFF00000000uLL;
    v1587[0] = v1596;
    if ( v1596 != nullptr )
      _InterlockedIncrement(v1596 + 2);
    v536 = sub_140E78C10(a1: v535, a2: v1587, a3: (unsigned int)v1585);
    v537 = (void (__fastcall ***)(_QWORD, __int64))v1587[0];
    if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] + 8LL)) == 0 )
      (**v537)(a1: v537, a2: 1);
    if ( (_BYTE)v536 != 0 )
    {
      v1578 = v434;
      LODWORD(v1582) = v536;
      v538 = a1[6];
      v539 = (__int64 *)a1[7];
      v540 = (__int64)v539 - v538;
      v541 = (__int64 *)v538;
      if ( (__int64)v539 - v538 > 0 )
      {
        v542 = (unsigned __int64)v540 >> 3;
        v541 = (__int64 *)a1[6];
        v543 = (unsigned __int64)v540 >> 3;
        do
        {
          v543 = (unsigned __int64)v543 >> 1;
          if ( *(_DWORD *)(v541[v543] + 56) < *(_DWORD *)(v535 + 56) )
          {
            v541 += v543 + 1;
            v543 = v542 + ~v543;
          }
          v542 = v543;
        }
        while ( v543 > 0 );
      }
      if ( v541 == v539 )
      {
        v564 = v1603;
        if ( v539 != (__int64 *)v1603[8] )
        {
          *v539 = v535;
          v564[7] += 8LL;
          a1 = v564;
          goto LABEL_1046;
        }
        v567 = (v540 >> 3) + 1;
        v568 = (unsigned __int64)(v540 >> 3) >> 1;
        v569 = 0x1FFFFFFFFFFFFFFFLL - v568;
        v570 = (v540 >> 3) + v568;
        if ( v570 <= v567 )
          v570 = (v540 >> 3) + 1;
        if ( v540 >> 3 > v569 )
          v570 = 0x1FFFFFFFFFFFFFFFLL;
        v571 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v570);
        *(_QWORD *)(v571 + v540) = v535;
        v572 = (__int64 *)v564[7];
        sub_141758A00(a1: v571, a2: v564[6], a3: (char *)v539 - v564[6]);
        if ( v572 != v539 )
          sub_141758A00(a1: v571 + v540 + 8, a2: v539, a3: v564[7] - (_QWORD)v539);
        v573 = v564[6];
        LODWORD(v10) = (unsigned __int8)v1604;
        if ( v573 != 0 )
        {
          v574 = v564[8] - v573;
          if ( v574 == -1 )
            v574 = *(unsigned int *)(v573 - *(unsigned int *)(qword_141ABD470 + 48));
          if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
            && (v575 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v575) >> 3 > v574)
            && (v576 = *(_QWORD *)(v575 + 8 * v574)) != 0 )
          {
            MEMORY[0x1419475D8](a1: v576 + 32, a2: v573 - *(unsigned int *)(v576 + 120));
            v577 = *(_BYTE *)(v576 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v576 + 64)) != 0;
            v564 = v1603;
            if ( !v577 && *(_BYTE *)(v576 + 97) != 0 )
              sub_1412D33C0(a1: v576);
          }
          else
          {
            MEMORY[0x141948990](a1: v573 - *(unsigned int *)(qword_141ABD470 + 48));
            v564 = v1603;
          }
        }
        v564[6] = v571;
        v564[7] = v571 + 8 * v567;
        v564[8] = v571 + 8 * v570;
        a1 = v564;
      }
      else
      {
        v544 = ((__int64)v541 - v538) >> 3;
        if ( *(_DWORD *)(*v541 + 56) == *(_DWORD *)(v535 + 56) )
        {
          v545 = v540 >> 3;
          if ( v545 > v544 )
          {
            v546 = *(__int64 **)(v538 + 8 * v544);
            if ( v546 != nullptr )
            {
              sub_140E44A40(a1: v546 + 6);
              v547 = v546[5];
              if ( v547 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v547 - 4)) == 0 )
                sub_1412EC9A0(a1: v547 - 4);
              v548 = v546[4];
              v549 = v1603;
              if ( v548 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v548 - 4)) == 0 )
                sub_1412EC9A0(a1: v548 - 4);
              v550 = v546[3];
              if ( v550 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v550 - 4)) == 0 )
                sub_1412EC9A0(a1: v550 - 4);
              v551 = v546[2];
              if ( v551 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v551 - 4)) == 0 )
                sub_1412EC9A0(a1: v551 - 4);
              v552 = v546[1];
              if ( v552 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v552 - 4)) == 0 )
                sub_1412EC9A0(a1: v552 - 4);
              v553 = *v546;
              if ( *v546 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v553 - 4)) == 0 )
                sub_1412EC9A0(a1: v553 - 4);
              sub_140FE1E10(a1: v546);
              v538 = v549[6];
              v539 = (__int64 *)v549[7];
              v545 = ((__int64)v539 - v538) >> 3;
            }
          }
          v31 = v1605;
          if ( v545 <= v544 )
          {
            v554 = v544 + 1;
            v555 = v544 + 1 - v545;
            if ( v544 + 1 < v545 )
            {
              v1603[7] = v538 + 8 * v554;
            }
            else if ( v544 + 1 > v545 )
            {
              v556 = (v1603[8] - v538) >> 3;
              if ( v556 >= v554 )
              {
                v588 = v1603;
                sub_141758A10(a1: v539, a2: 0, a3: 8 * v555);
                v31 = v1605;
                v588[7] = &v539[v555];
                v538 = v588[6];
              }
              else
              {
                v263 = v554 >> 61;
                if ( v554 >> 61 != 0 )
                  goto LABEL_3115;
                v557 = v556 + (v556 >> 1);
                if ( v557 <= v554 )
                  v557 = v544 + 1;
                if ( v556 > 0x1FFFFFFFFFFFFFFFLL - (v556 >> 1) )
                  v557 = 0x1FFFFFFFFFFFFFFFLL;
                v538 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v557);
                sub_141758A10(a1: v538 + 8 * v545, a2: 0, a3: 8 * v555);
                v558 = v1603;
                sub_141758A00(a1: v538, a2: v1603[6], a3: v1603[7] - v1603[6]);
                v559 = v558[6];
                if ( v559 != 0 )
                {
                  v560 = v558[8] - v559;
                  if ( v560 == -1 )
                    v560 = *(unsigned int *)(v559 - *(unsigned int *)(qword_141ABD470 + 48));
                  if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                    && (v561 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v561) >> 3 > v560)
                    && (v562 = *(_QWORD *)(v561 + 8 * v560)) != 0 )
                  {
                    MEMORY[0x1419475D8](a1: v562 + 32, a2: v559 - *(unsigned int *)(v562 + 120));
                    v563 = *(_BYTE *)(v562 + 72) != 0
                        && _InterlockedDecrement((volatile signed __int32 *)(v562 + 64)) != 0;
                    if ( !v563 && *(_BYTE *)(v562 + 97) != 0 )
                      sub_1412D33C0(a1: v562);
                  }
                  else
                  {
                    MEMORY[0x141948990](a1: v559 - *(unsigned int *)(qword_141ABD470 + 48));
                  }
                }
                v558[6] = v538;
                v558[7] = v538 + 8 * (v544 + 1);
                v558[8] = v538 + 8 * v557;
                v31 = v1605;
              }
            }
          }
          *(_QWORD *)(v538 + 8 * v544) = v535;
          a1 = v1603;
          LODWORD(v10) = (unsigned __int8)v1604;
          goto LABEL_955;
        }
        v565 = (__int64 *)(v538 + 8 * v544);
        v566 = v1603;
        if ( v539 == (__int64 *)v1603[8] )
        {
          v578 = v540 >> 3;
          v579 = v578 + 1;
          v580 = v578 + (v578 >> 1);
          if ( v580 <= v578 + 1 )
            v580 = v578 + 1;
          if ( v578 > 0x1FFFFFFFFFFFFFFFLL - (v578 >> 1) )
            v580 = 0x1FFFFFFFFFFFFFFFLL;
          v581 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v580);
          *(_QWORD *)(v581 + 8 * v544) = v535;
          v582 = (__int64 *)v566[7];
          sub_141758A00(a1: v581, a2: v566[6], a3: (char *)v565 - v566[6]);
          if ( v582 != v565 )
            sub_141758A00(a1: v581 + 8 * v544 + 8, a2: v565, a3: v566[7] - (_QWORD)v565);
          v583 = v566[6];
          a1 = v566;
          if ( v583 != 0 )
          {
            v584 = v566[8] - v583;
            if ( v584 == -1 )
              v584 = *(unsigned int *)(v583 - *(unsigned int *)(qword_141ABD470 + 48));
            if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
              && (v585 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v585) >> 3 > v584)
              && (v586 = *(_QWORD *)(v585 + 8 * v584)) != 0 )
            {
              MEMORY[0x1419475D8](a1: v586 + 32, a2: v583 - *(unsigned int *)(v586 + 120));
              v587 = *(_BYTE *)(v586 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v586 + 64)) != 0;
              if ( !v587 && *(_BYTE *)(v586 + 97) != 0 )
                sub_1412D33C0(a1: v586);
            }
            else
            {
              MEMORY[0x141948990](a1: v583 - *(unsigned int *)(qword_141ABD470 + 48));
            }
          }
          v566[6] = v581;
          v566[7] = v581 + 8 * v579;
          v566[8] = v581 + 8 * v580;
        }
        else if ( v539 == v565 )
        {
          *v539 = v535;
          a1 = v1603;
          v1603[7] += 8LL;
        }
        else
        {
          *v539 = *(v539 - 1);
          a1 = v1603;
          v1603[7] += 8LL;
          sub_141758A00(a1: v565 + 1, a2: v565, a3: (char *)(v539 - 1) - (char *)v565);
          *v565 = v535;
        }
LABEL_1046:
        LODWORD(v10) = (unsigned __int8)v1604;
      }
      v31 = v1605;
LABEL_955:
      LOBYTE(v83) = v1582;
      v434 = v1578 + 1;
      LODWORD(v32) = a5;
      if ( v1578 + 1 >= (int)v1600 )
        goto LABEL_85;
      continue;
    }
    break;
  }
  LOBYTE(v83) = 0;
  LODWORD(v10) = (unsigned __int8)v1604;
  v31 = v1605;
  LODWORD(v32) = a5;
LABEL_85:
  v84 = v1596;
  if ( v1596 != nullptr && _InterlockedDecrement(v1596 + 2) == 0 )
  {
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v84)(a1: v84, a2: 1);
    v31 = v1605;
  }
  v33 = a9;
  if ( (_BYTE)v83 == 0 )
    goto LABEL_2936;
LABEL_89:
  v85 = v33 & v31;
  if ( (_BYTE)v32 == 0 )
  {
    LOBYTE(v32) = 1;
    if ( a6 == 0 || (_BYTE)v1597 != 0 )
      return (unsigned int)v32;
    goto LABEL_95;
  }
  v1605 = v33 & v31;
  if ( (v31 & (unsigned __int8)(v10 & v1599)) == 0 )
    goto LABEL_134;
  v86 = *((_DWORD *)a1 + 92);
  v32 = (__int64)&v1595;
  sub_14080D0E0(a1: &v1595, a2: 0x1418E2C24LL);
  LODWORD(v1599) = v86;
  LODWORD(v1593) = v86;
  v1594 = 25;
  sub_1408085A0(a1: &v1579, a2: &v1594);
  sub_1408085A0(a1: &v1602, a2: &v1593);
  v1600 = nullptr;
  v87 = v1602;
  if ( v1602 != nullptr )
  {
    _InterlockedIncrement(v1602 - 1);
    v1600 = v87;
    v88 = *v87;
  }
  else
  {
    v88 = 0;
  }
  v10 = (__int64)a1;
  v93 = v88 + 1;
  v94 = sub_1412EC810(a1: 264, a2: (unsigned int)(v88 + 1));
  v95 = (volatile signed __int32 *)v94;
  *(_DWORD *)v94 = 0;
  v96 = 0;
  if ( v88 + 1 <= 0 )
    v93 = 0;
  *(_DWORD *)(v94 + 4) = v93;
  v97 = v94 + 8;
  *(_BYTE *)(v94 + 8) = 0;
  if ( v88 <= 0 )
  {
    v99 = (_BYTE *)(v94 + 8);
    if ( v88 == 0 )
      goto LABEL_105;
  }
  else
  {
    v98 = 0x1419435F1LL;
    if ( v1600 != nullptr )
      v98 = (__int64)(v1600 + 1);
    sub_141758A00(a1: v94 + 8, a2: v98, a3: (unsigned int)v88);
    v99 = (_BYTE *)(v97 + (unsigned int)v88);
LABEL_105:
    *v99 = 0;
    v96 = v88;
  }
  v100 = (volatile signed __int32 *)(v94 + 4);
  *(_WORD *)(v97 + v96) = 95;
  v101 = v1600 - 1;
  if ( v1600 != nullptr && _InterlockedDecrement(v101) == 0 )
    sub_1412EC9A0(a1: v101);
  v1600 = nullptr;
  _InterlockedIncrement(v95);
  v1600 = v100;
  sub_140809550(a1: &v1600, a2: v1587, a3: &v1579);
  v1583 = 0;
  v102 = v1587[0];
  if ( v1587[0] != 0 )
  {
    _InterlockedIncrement((volatile signed __int32 *)(v1587[0] - 4LL));
    v103 = v1587[0];
    v1583 = v102;
    if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] - 4LL)) == 0 )
      sub_1412EC9A0(a1: v103 - 4);
  }
  v104 = v1600;
  v105 = (_QWORD *)v10;
  if ( v1600 != nullptr && _InterlockedDecrement(v1600 - 1) == 0 )
    sub_1412EC9A0(a1: v104 - 1);
  v106 = v1602;
  if ( v1602 != nullptr && _InterlockedDecrement(v1602 - 1) == 0 )
    sub_1412EC9A0(a1: v106 - 1);
  v107 = v1579;
  if ( v1579 != nullptr && _InterlockedDecrement(v1579 - 1) == 0 )
    sub_1412EC9A0(a1: v107 - 1);
  v1587[0] = 0x80100004E554C4CLL;
  LOBYTE(v1553) = 0;
  sub_1407D0F70(
    a1: (unsigned int)v1587,
    a2: (unsigned int)&v1596,
    a3: a2,
    a4: (unsigned int)&v1583,
    a5: (__int64)&v1595,
    a6: 0,
    a7: 0,
    v1553);
  v108 = v1583;
  if ( v1583 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1583 - 4)) == 0 )
    sub_1412EC9A0(a1: v108 - 4);
  v109 = v1596;
  if ( v1596 == nullptr )
    goto LABEL_2936;
  v110 = *(_QWORD *)(v10 + 80) != *(_QWORD *)(v10 + 72);
  LODWORD(v1600) = 0;
  (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **, __int64))(*(_QWORD *)v1596 + 40LL))(
    a1: v1596,
    a2: &v1600,
    a3: 4);
  if ( *((_DWORD *)v109 + 4) != 0 )
  {
    v111 = (_QWORD *)v10;
    LOBYTE(v112) = 0;
LABEL_129:
    LODWORD(v10) = (unsigned __int8)v1604;
    goto LABEL_130;
  }
  if ( v1601 == 0 )
  {
    v252 = (int)v1600;
    v253 = v110;
    if ( v110 )
    {
      v254 = *(_QWORD *)(v10 + 72);
      v255 = (*(_QWORD *)(v10 + 80) - v254) >> 3;
      v256 = v255 + (int)v1600;
      v257 = (*(_QWORD *)(v10 + 88) - v254) >> 3;
      LODWORD(v10) = (unsigned __int8)v1604;
      if ( v257 < v256 )
      {
        if ( v256 >> 61 == 0 )
        {
          v32 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v256);
          sub_141758A00(a1: v32, a2: v105[9], a3: v105[10] - v105[9]);
          if ( v105[9] != 0 )
            sub_1407E4890(a1: qword_141ABD470);
          v105[9] = v32;
          v105[10] = v32 + 8 * v255;
          v105[11] = v32 + 8 * v256;
          goto LABEL_696;
        }
LABEL_3114:
        sub_1400526C0(a1: v257);
      }
    }
    else
    {
      v32 = *(_QWORD *)(v10 + 72);
      v257 = (*(_QWORD *)(v10 + 88) - v32) >> 3;
      LODWORD(v10) = (unsigned __int8)v1604;
      if ( v257 < (int)v1600 )
      {
        if ( (int)v1600 >= 0 )
        {
          v404 = v105[10];
          v405 = v105;
          v406 = sub_1407E4490(a1: qword_141ABD470, a2: 8LL * (int)v1600);
          sub_141758A00(a1: v406, a2: v405[9], a3: v405[10] - v405[9]);
          if ( v405[9] != 0 )
            sub_1407E4890(a1: qword_141ABD470);
          v405[9] = v406;
          v405[10] = v406 + v404 - v32;
          v405[11] = v406 + 8 * v252;
          v105 = v405;
          goto LABEL_696;
        }
        goto LABEL_3114;
      }
    }
LABEL_696:
    if ( (int)v1600 <= 0 )
    {
      v111 = v105;
      LOBYTE(v112) = 1;
      goto LABEL_130;
    }
    if ( !v253 )
    {
      v111 = v105;
      v601 = 0;
      do
      {
        if ( dword_141B60AD0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                         + 4LL) )
        {
          sub_141750E08(a1: &dword_141B60AD0);
          if ( dword_141B60AD0 == -1 )
          {
            sub_1407E53D0(
              a1: (unsigned int)&unk_141B60A80,
              a2: 1100150629,
              a3: 1280,
              a4: 40,
              a5: 0,
              a6: 1,
              a7: 1280,
              a8: 4096);
            sub_141751048(a1: sub_140FE1E00);
            sub_141750EA0(a1: &dword_141B60AD0);
          }
        }
        v602 = sub_1407E58C0(a1: &unk_141B60A80, a2: 40);
        *(_QWORD *)v602 = 0;
        *(_QWORD *)(v602 + 8) = 0;
        *(_QWORD *)(v602 + 16) = 0;
        *(_QWORD *)(v602 + 24) = 0;
        *(_WORD *)(v602 + 36) = -1;
        *(_DWORD *)(v602 + 32) = 0;
        v1587[0] = v1596;
        if ( v1596 != nullptr )
          _InterlockedIncrement(v1596 + 2);
        LODWORD(v112) = sub_140EBDAB0(a1: v602, a2: v1587, a3: (unsigned int)v1599);
        v603 = (void (__fastcall ***)(_QWORD, __int64))v1587[0];
        if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] + 8LL)) == 0 )
          (**v603)(a1: v603, a2: 1);
        if ( (_BYTE)v112 == 0 )
          break;
        v32 = (__int64)v111;
        v604 = (__int64 *)v111[10];
        if ( v604 == (__int64 *)v111[11] )
        {
          LODWORD(v1585) = v112;
          v605 = (__int64)v604 - v111[9];
          v606 = v605 >> 3;
          v607 = (unsigned __int64)(v605 >> 3) >> 1;
          v608 = 0x1FFFFFFFFFFFFFFFLL - v607;
          v609 = (v605 >> 3) + v607;
          v1582 = (v605 >> 3) + 1;
          if ( v609 <= v1582 )
            v609 = v606 + 1;
          if ( v606 > v608 )
            v609 = 0x1FFFFFFFFFFFFFFFLL;
          v112 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v609);
          *(_QWORD *)(v112 + v605) = v602;
          v610 = *(__int64 **)(v32 + 80);
          sub_141758A00(a1: v112, a2: *(_QWORD *)(v32 + 72), a3: (char *)v604 - *(_QWORD *)(v32 + 72));
          if ( v610 != v604 )
            sub_141758A00(a1: v112 + v605 + 8, a2: v604, a3: *(_QWORD *)(v32 + 80) - (_QWORD)v604);
          v611 = *(_QWORD *)(v32 + 72);
          v612 = (_QWORD *)v32;
          LODWORD(v10) = (unsigned __int8)v1604;
          if ( v611 != 0 )
          {
            v613 = *(_QWORD *)(v32 + 88) - v611;
            if ( v613 == -1 )
              v613 = *(unsigned int *)(v611 - *(unsigned int *)(qword_141ABD470 + 48));
            if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
              && (v614 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v614) >> 3 > v613)
              && (v32 = *(_QWORD *)(v614 + 8 * v613)) != 0 )
            {
              MEMORY[0x1419475D8](a1: v32 + 32, a2: v611 - *(unsigned int *)(v32 + 120));
              v615 = *(_BYTE *)(v32 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v32 + 64)) != 0;
              v612 = v1603;
              if ( !v615 && *(_BYTE *)(v32 + 97) != 0 )
                sub_1412D33C0(a1: v32);
            }
            else
            {
              MEMORY[0x141948990](a1: v611 - *(unsigned int *)(qword_141ABD470 + 48));
              v612 = v1603;
            }
          }
          v612[9] = v112;
          v612[10] = v112 + 8 * v1582;
          v612[11] = v112 + 8 * v609;
          v111 = v612;
          LOBYTE(v112) = v1585;
        }
        else
        {
          *v604 = v602;
          v111[10] += 8LL;
        }
        ++v601;
      }
      while ( v601 < (int)v1600 );
      goto LABEL_130;
    }
    v407 = 0;
    while ( 1 )
    {
      if ( dword_141B60AD0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(a1: &dword_141B60AD0);
        if ( dword_141B60AD0 == -1 )
        {
          sub_1407E53D0(
            a1: (unsigned int)&unk_141B60A80,
            a2: 1100150629,
            a3: 1280,
            a4: 40,
            a5: 0,
            a6: 1,
            a7: 1280,
            a8: 4096);
          sub_141751048(a1: sub_140FE1E00);
          sub_141750EA0(a1: &dword_141B60AD0);
        }
      }
      v466 = sub_1407E58C0(a1: &unk_141B60A80, a2: 40);
      *(_QWORD *)v466 = 0;
      *(_QWORD *)(v466 + 8) = 0;
      *(_QWORD *)(v466 + 16) = 0;
      *(_QWORD *)(v466 + 24) = 0;
      *(_WORD *)(v466 + 36) = -1;
      *(_DWORD *)(v466 + 32) = 0;
      v1587[0] = v1596;
      if ( v1596 != nullptr )
        _InterlockedIncrement(v1596 + 2);
      v467 = sub_140EBDAB0(a1: v466, a2: v1587, a3: (unsigned int)v1599);
      v468 = (void (__fastcall ***)(_QWORD, __int64))v1587[0];
      if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] + 8LL)) == 0 )
        (**v468)(a1: v468, a2: 1);
      if ( (_BYTE)v467 == 0 )
      {
        LOBYTE(v112) = 0;
        v111 = v1603;
        goto LABEL_130;
      }
      LODWORD(v1582) = v407;
      LODWORD(v1585) = v467;
      v469 = v1603[9];
      v470 = (__int64 *)v1603[10];
      v32 = (__int64)v470 - v469;
      v471 = (__int64 *)v469;
      if ( (__int64)v470 - v469 > 0 )
      {
        v472 = (unsigned __int64)v32 >> 3;
        v471 = (__int64 *)v1603[9];
        v473 = (unsigned __int64)v32 >> 3;
        do
        {
          v473 = (unsigned __int64)v473 >> 1;
          if ( *(_DWORD *)(v471[v473] + 32) < *(_DWORD *)(v466 + 32) )
          {
            v471 += v473 + 1;
            v473 = v472 + ~v473;
          }
          v472 = v473;
        }
        while ( v473 > 0 );
      }
      if ( v471 == v470 )
      {
        v10 = (__int64)v1603;
        if ( v470 == (__int64 *)v1603[11] )
        {
          v491 = (unsigned __int64)(v32 >> 3) >> 1;
          v492 = 0x1FFFFFFFFFFFFFFFLL - v491;
          v493 = (v32 >> 3) + v491;
          v1577 = (v32 >> 3) + 1;
          if ( v493 <= v1577 )
            v493 = (v32 >> 3) + 1;
          if ( v32 >> 3 > v492 )
            v493 = 0x1FFFFFFFFFFFFFFFLL;
          v494 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v493);
          *(_QWORD *)(v494 + v32) = v466;
          v495 = v494;
          v496 = *(__int64 **)(v10 + 80);
          sub_141758A00(a1: v494, a2: *(_QWORD *)(v10 + 72), a3: (char *)v470 - *(_QWORD *)(v10 + 72));
          v497 = (_QWORD *)v10;
          if ( v496 != v470 )
          {
            v32 += v495 + 8;
            sub_141758A00(a1: v32, a2: v470, a3: *(_QWORD *)(v10 + 80) - (_QWORD)v470);
          }
          v498 = *(_QWORD *)(v10 + 72);
          LODWORD(v10) = (unsigned __int8)v1604;
          if ( v498 != 0 )
          {
            v499 = v497[11] - v498;
            if ( v499 == -1 )
              v499 = *(unsigned int *)(v498 - *(unsigned int *)(qword_141ABD470 + 48));
            if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
              && (v500 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v500) >> 3 > v499)
              && (v32 = *(_QWORD *)(v500 + 8 * v499)) != 0 )
            {
              MEMORY[0x1419475D8](a1: v32 + 32, a2: v498 - *(unsigned int *)(v32 + 120));
              v501 = *(_BYTE *)(v32 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v32 + 64)) != 0;
              if ( !v501 && *(_BYTE *)(v32 + 97) != 0 )
                sub_1412D33C0(a1: v32);
            }
            else
            {
              MEMORY[0x141948990](a1: v498 - *(unsigned int *)(qword_141ABD470 + 48));
            }
          }
          v497[9] = v495;
          v497[10] = v495 + 8 * v1577;
          v511 = v495 + 8 * v493;
          v111 = v497;
          v497[11] = v511;
          goto LABEL_814;
        }
        *v470 = v466;
        *(_QWORD *)(v10 + 80) += 8LL;
        v111 = (_QWORD *)v10;
      }
      else
      {
        v474 = ((__int64)v471 - v469) >> 3;
        if ( *(_DWORD *)(*v471 + 32) == *(_DWORD *)(v466 + 32) )
        {
          v32 >>= 3;
          if ( v32 > v474 )
          {
            v475 = *(__int64 **)(v469 + 8 * v474);
            if ( v475 != nullptr )
            {
              sub_140E44A40(a1: v475 + 3);
              v476 = v475[2];
              if ( v476 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v476 - 4)) == 0 )
                sub_1412EC9A0(a1: v476 - 4);
              v477 = v475[1];
              if ( v477 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v477 - 4)) == 0 )
                sub_1412EC9A0(a1: v477 - 4);
              v478 = *v475;
              if ( *v475 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v478 - 4)) == 0 )
                sub_1412EC9A0(a1: v478 - 4);
              sub_140FE1CA0(a1: v475);
              v469 = v1603[9];
              v470 = (__int64 *)v1603[10];
              v32 = ((__int64)v470 - v469) >> 3;
            }
          }
          if ( v32 <= v474 )
          {
            v479 = v474 + 1;
            v480 = v474 + 1 - v32;
            if ( v474 + 1 < v32 )
            {
              v1603[10] = v469 + 8 * v479;
            }
            else if ( v474 + 1 > v32 )
            {
              v481 = (v1603[11] - v469) >> 3;
              if ( v481 >= v479 )
              {
                v512 = v1603;
                sub_141758A10(a1: v470, a2: 0, a3: 8 * v480);
                v512[10] = &v470[v480];
                v469 = v512[9];
              }
              else
              {
                v257 = v479 >> 61;
                if ( v479 >> 61 != 0 )
                  goto LABEL_3114;
                v482 = v481 + (v481 >> 1);
                if ( v482 <= v479 )
                  v482 = v474 + 1;
                if ( v481 > 0x1FFFFFFFFFFFFFFFLL - (v481 >> 1) )
                  v482 = 0x1FFFFFFFFFFFFFFFLL;
                v469 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v482);
                sub_141758A10(a1: v469 + 8 * v32, a2: 0, a3: 8 * v480);
                v483 = v1603;
                sub_141758A00(a1: v469, a2: v1603[9], a3: v1603[10] - v1603[9]);
                v484 = v483[9];
                if ( v484 != 0 )
                {
                  v485 = v483[11] - v484;
                  if ( v485 == -1 )
                    v485 = *(unsigned int *)(v484 - *(unsigned int *)(qword_141ABD470 + 48));
                  if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                    && (v486 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v486) >> 3 > v485)
                    && (v32 = *(_QWORD *)(v486 + 8 * v485)) != 0 )
                  {
                    MEMORY[0x1419475D8](a1: v32 + 32, a2: v484 - *(unsigned int *)(v32 + 120));
                    v487 = *(_BYTE *)(v32 + 72) != 0
                        && _InterlockedDecrement((volatile signed __int32 *)(v32 + 64)) != 0;
                    v483 = v1603;
                    if ( !v487 && *(_BYTE *)(v32 + 97) != 0 )
                      sub_1412D33C0(a1: v32);
                  }
                  else
                  {
                    MEMORY[0x141948990](a1: v484 - *(unsigned int *)(qword_141ABD470 + 48));
                    v483 = v1603;
                  }
                }
                v483[9] = v469;
                v483[10] = v469 + 8 * (v474 + 1);
                v483[11] = v469 + 8 * v482;
              }
            }
          }
          *(_QWORD *)(v469 + 8 * v474) = v466;
          v111 = v1603;
        }
        else
        {
          v488 = (__int64 *)(v469 + 8 * v474);
          v489 = v1603;
          if ( v470 == (__int64 *)v1603[11] )
          {
            v502 = v32 >> 3;
            v503 = v502 + 1;
            v504 = v502 + (v502 >> 1);
            if ( v504 <= v502 + 1 )
              v504 = v502 + 1;
            if ( v502 > 0x1FFFFFFFFFFFFFFFLL - (v502 >> 1) )
              v504 = 0x1FFFFFFFFFFFFFFFLL;
            v32 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v504);
            *(_QWORD *)(v32 + 8 * v474) = v466;
            v505 = (__int64 *)v489[10];
            sub_141758A00(a1: v32, a2: v489[9], a3: (char *)v488 - v489[9]);
            v390 = v505 == v488;
            v111 = v489;
            if ( !v390 )
              sub_141758A00(a1: v32 + 8 * v474 + 8, a2: v488, a3: v489[10] - (_QWORD)v488);
            v506 = v489[9];
            LODWORD(v10) = (unsigned __int8)v1604;
            if ( v506 != 0 )
            {
              v507 = v111[11] - v506;
              if ( v507 == -1 )
                v507 = *(unsigned int *)(v506 - *(unsigned int *)(qword_141ABD470 + 48));
              if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                && (v508 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v508) >> 3 > v507)
                && (v509 = *(_QWORD *)(v508 + 8 * v507)) != 0 )
              {
                MEMORY[0x1419475D8](a1: v509 + 32, a2: v506 - *(unsigned int *)(v509 + 120));
                v510 = *(_BYTE *)(v509 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v509 + 64)) != 0;
                LODWORD(v10) = (unsigned __int8)v1604;
                if ( !v510 && *(_BYTE *)(v509 + 97) != 0 )
                  sub_1412D33C0(a1: v509);
              }
              else
              {
                MEMORY[0x141948990](a1: v506 - *(unsigned int *)(qword_141ABD470 + 48));
                LODWORD(v10) = (unsigned __int8)v1604;
              }
            }
            v111[9] = v32;
            v111[10] = v32 + 8 * v503;
            v111[11] = v32 + 8 * v504;
            goto LABEL_814;
          }
          if ( v470 == v488 )
          {
            *v470 = v466;
            v111 = v1603;
            v1603[10] += 8LL;
          }
          else
          {
            *v470 = *(v470 - 1);
            v490 = v1603;
            v1603[10] += 8LL;
            sub_141758A00(a1: v488 + 1, a2: v488, a3: (char *)(v470 - 1) - (char *)v488);
            *v488 = v466;
            v111 = v490;
          }
        }
      }
      LODWORD(v10) = (unsigned __int8)v1604;
LABEL_814:
      LOBYTE(v112) = v1585;
      v407 = v1582 + 1;
      if ( (int)v1582 + 1 >= (int)v1600 )
        goto LABEL_130;
    }
  }
  LOBYTE(v112) = 1;
  if ( (int)v1600 <= 0 )
  {
    v111 = (_QWORD *)v10;
    goto LABEL_129;
  }
  v147 = 0;
  v32 = (__int64)&v1587[3];
  while ( 1 )
  {
    memset(v1587, 0, sizeof(v1587));
    WORD2(v1588) = -1;
    LODWORD(v1588) = 0;
    v1579 = v1596;
    if ( v1596 != nullptr )
      _InterlockedIncrement(v1596 + 2);
    v148 = sub_140EBDAB0(a1: v1587, a2: &v1579, a3: (unsigned int)v1599);
    v149 = v1579;
    if ( v1579 != nullptr && _InterlockedDecrement(v1579 + 2) == 0 )
      (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v149)(a1: v149, a2: 1);
    if ( v148 == 0 )
      break;
    sub_140EBD850(a1: v1587);
    sub_140E44A40(a1: &v1587[3]);
    v150 = v1587[2];
    if ( v1587[2] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[2] - 4LL)) == 0 )
      sub_1412EC9A0(a1: v150 - 4);
    v151 = v1587[1];
    if ( v1587[1] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[1] - 4LL)) == 0 )
      sub_1412EC9A0(a1: v151 - 4);
    v152 = v1587[0];
    if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] - 4LL)) == 0 )
      sub_1412EC9A0(a1: v152 - 4);
    if ( ++v147 >= (int)v1600 )
    {
      v111 = (_QWORD *)v10;
      LODWORD(v10) = (unsigned __int8)v1604;
      LOBYTE(v112) = 1;
      goto LABEL_130;
    }
  }
  sub_140E44A40(a1: &v1587[3]);
  v598 = v1587[2];
  if ( v1587[2] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[2] - 4LL)) == 0 )
    sub_1412EC9A0(a1: v598 - 4);
  v599 = v1587[1];
  v111 = (_QWORD *)v10;
  if ( v1587[1] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[1] - 4LL)) == 0 )
    sub_1412EC9A0(a1: v599 - 4);
  v600 = v1587[0];
  LODWORD(v10) = (unsigned __int8)v1604;
  if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] - 4LL)) == 0 )
    sub_1412EC9A0(a1: v600 - 4);
  LOBYTE(v112) = 0;
LABEL_130:
  v113 = v1596;
  if ( v1596 != nullptr && _InterlockedDecrement(v1596 + 2) == 0 )
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v113)(a1: v113, a2: 1);
  v85 = v1605;
  a1 = v111;
  if ( (_BYTE)v112 == 0 )
    goto LABEL_2936;
LABEL_134:
  if ( (v85 & (unsigned __int8)(v10 & v1598)) == 0 )
    goto LABEL_194;
  v114 = *((_DWORD *)a1 + 92);
  v32 = (__int64)&v1595;
  sub_14080D0E0(a1: &v1595, a2: 0x1418E2C24LL);
  LODWORD(v1593) = v114;
  v1594 = 2;
  sub_1408085A0(a1: &v1579, a2: &v1594);
  sub_1408085A0(a1: &v1602, a2: &v1593);
  v1600 = nullptr;
  v115 = v1602;
  if ( v1602 != nullptr )
  {
    _InterlockedIncrement(v1602 - 1);
    v1600 = v115;
    v116 = *v115;
  }
  else
  {
    v116 = 0;
  }
  v124 = a1;
  v125 = v116 + 1;
  v126 = sub_1412EC810(a1: 264, a2: (unsigned int)(v116 + 1));
  v127 = (volatile signed __int32 *)v126;
  *(_DWORD *)v126 = 0;
  v128 = 0;
  if ( v116 + 1 <= 0 )
    v125 = 0;
  *(_DWORD *)(v126 + 4) = v125;
  v129 = v126 + 8;
  *(_BYTE *)(v126 + 8) = 0;
  if ( v116 <= 0 )
  {
    v131 = (_BYTE *)(v126 + 8);
    if ( v116 == 0 )
      goto LABEL_166;
  }
  else
  {
    v130 = 0x1419435F1LL;
    if ( v1600 != nullptr )
      v130 = (__int64)(v1600 + 1);
    sub_141758A00(a1: v126 + 8, a2: v130, a3: (unsigned int)v116);
    v131 = (_BYTE *)(v129 + (unsigned int)v116);
LABEL_166:
    *v131 = 0;
    v128 = v116;
  }
  v132 = (volatile signed __int32 *)(v126 + 4);
  *(_WORD *)(v129 + v128) = 95;
  v133 = v1600 - 1;
  if ( v1600 != nullptr && _InterlockedDecrement(v133) == 0 )
    sub_1412EC9A0(a1: v133);
  v1600 = nullptr;
  _InterlockedIncrement(v127);
  v1600 = v132;
  sub_140809550(a1: &v1600, a2: v1587, a3: &v1579);
  v1583 = 0;
  v134 = v1587[0];
  if ( v1587[0] != 0 )
  {
    _InterlockedIncrement((volatile signed __int32 *)(v1587[0] - 4LL));
    v135 = v1587[0];
    v1583 = v134;
    if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] - 4LL)) == 0 )
      sub_1412EC9A0(a1: v135 - 4);
  }
  v136 = v1600;
  a1 = v124;
  if ( v1600 != nullptr && _InterlockedDecrement(v1600 - 1) == 0 )
    sub_1412EC9A0(a1: v136 - 1);
  v137 = v1602;
  LODWORD(v10) = (unsigned __int8)v1604;
  if ( v1602 != nullptr && _InterlockedDecrement(v1602 - 1) == 0 )
    sub_1412EC9A0(a1: v137 - 1);
  v138 = v1579;
  if ( v1579 != nullptr && _InterlockedDecrement(v1579 - 1) == 0 )
    sub_1412EC9A0(a1: v138 - 1);
  v1587[0] = 0x80100004E554C4CLL;
  LOBYTE(v1553) = 0;
  sub_1407D0F70(
    a1: (unsigned int)v1587,
    a2: (unsigned int)&v1596,
    a3: a2,
    a4: (unsigned int)&v1583,
    a5: (__int64)&v1595,
    a6: 0,
    a7: 0,
    v1553);
  v139 = v1583;
  if ( v1583 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1583 - 4)) == 0 )
    sub_1412EC9A0(a1: v139 - 4);
  v140 = v1596;
  if ( v1596 == nullptr )
    goto LABEL_2936;
  v141 = a1[4] != a1[3];
  LODWORD(v1602) = 0;
  (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **, __int64))(*(_QWORD *)v1596 + 40LL))(
    a1: v1596,
    a2: &v1602,
    a3: 4);
  if ( *((_DWORD *)v140 + 4) != 0 )
  {
    v142 = 0;
    goto LABEL_190;
  }
  if ( v1601 != 0 )
  {
    v142 = 1;
    if ( (int)v1602 <= 0 )
      goto LABEL_190;
    v32 = (__int64)&v1587[2];
    v215 = 0;
    while ( 2 )
    {
      memset(v1587, 0, 21);
      v1579 = v1596;
      _InterlockedIncrement(v1596 + 2);
      v216 = v1579;
      (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *, __int64))(*(_QWORD *)v1579 + 40LL))(
        a1: v1579,
        a2: &v1587[2],
        a3: 4);
      if ( *((_DWORD *)v216 + 4) != 0 || (sub_140814B10(a1: v1579, a2: &v1600, a3: v1587), (_DWORD)v1600 != 0) )
      {
        v217 = v10;
        goto LABEL_335;
      }
      v217 = v10;
      v222 = v1579;
      (*(void (__fastcall **)(volatile signed __int32 *, char *, __int64))(*(_QWORD *)v1579 + 40LL))(
        a1: v1579,
        a2: (char *)&v1587[2] + 4,
        a3: 1);
      if ( *((_DWORD *)v222 + 4) != 0 )
LABEL_335:
        v218 = 0;
      else
        v218 = sub_140E45290(a1: &v1587[1], a2: &v1579);
      v219 = v1579;
      if ( v1579 != nullptr && _InterlockedDecrement(v1579 + 2) == 0 )
        (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v219)(a1: v219, a2: 1);
      if ( v218 == 0 )
      {
        sub_140E44A40(a1: &v1587[1]);
        v756 = v1587[0];
        v757 = v1603;
        LODWORD(v10) = v217;
        if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] - 4LL)) == 0 )
          sub_1412EC9A0(a1: v756 - 4);
        v142 = 0;
        a1 = v757;
        goto LABEL_190;
      }
      sub_140E56800(a1: v1587);
      sub_140E44A40(a1: &v1587[1]);
      v220 = v1587[0];
      v221 = v1603;
      LODWORD(v10) = v217;
      if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] - 4LL)) == 0 )
        sub_1412EC9A0(a1: v220 - 4);
      if ( ++v215 >= (int)v1602 )
      {
        a1 = v221;
        v142 = 1;
        goto LABEL_190;
      }
      continue;
    }
  }
  v326 = (int)v1602;
  v327 = v141;
  if ( v141 )
  {
    v328 = a1[3];
    v329 = (a1[4] - v328) >> 3;
    v330 = v329 + (int)v1602;
    v331 = (a1[5] - v328) >> 3;
    if ( v331 >= v330 )
      goto LABEL_1077;
    if ( v330 >> 61 == 0 )
    {
      v32 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v330);
      sub_141758A00(a1: v32, a2: a1[3], a3: a1[4] - a1[3]);
      if ( a1[3] != 0 )
        sub_1407E4890(a1: qword_141ABD470);
      a1[3] = v32;
      a1[4] = v32 + 8 * v329;
      a1[5] = v32 + 8 * v330;
      goto LABEL_1077;
    }
LABEL_3116:
    sub_1400526C0(a1: v331);
  }
  v32 = a1[3];
  v331 = (a1[5] - v32) >> 3;
  if ( v331 < (int)v1602 )
  {
    if ( (int)v1602 < 0 )
      goto LABEL_3116;
    v594 = a1[4];
    v595 = a1;
    v596 = sub_1407E4490(a1: qword_141ABD470, a2: 8LL * (int)v1602);
    sub_141758A00(a1: v596, a2: v595[3], a3: v595[4] - v595[3]);
    if ( v595[3] != 0 )
      sub_1407E4890(a1: qword_141ABD470);
    v595[3] = v596;
    v595[4] = v596 + v594 - v32;
    v595[5] = v596 + 8 * v326;
    a1 = v595;
  }
LABEL_1077:
  if ( (int)v1602 <= 0 )
  {
    v142 = 1;
    goto LABEL_190;
  }
  if ( !v327 )
  {
    v758 = 0;
    v32 = (__int64)&unk_141B60B30;
    while ( 1 )
    {
      if ( dword_141B60B80 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(a1: &dword_141B60B80);
        if ( dword_141B60B80 == -1 )
        {
          sub_1407E53D0(
            a1: (unsigned int)&unk_141B60B30,
            a2: 1100150566,
            a3: 2048,
            a4: 24,
            a5: 0,
            a6: 1,
            a7: 2048,
            a8: 4096);
          sub_141751048(a1: sub_140FE20E0);
          sub_141750EA0(a1: &dword_141B60B80);
        }
      }
      v759 = (_QWORD *)sub_1407E58C0(a1: &unk_141B60B30, a2: 24);
      *v759 = 0;
      v759[1] = 0;
      *(_QWORD *)((char *)v759 + 13) = 0;
      v1587[0] = v1596;
      _InterlockedIncrement(v1596 + 2);
      v760 = v1587[0];
      (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)v1587[0] + 40LL))(
        a1: v1587[0],
        a2: v759 + 2,
        a3: 4);
      if ( *(_DWORD *)(v760 + 16) != 0
        || (sub_140814B10(a1: v1587[0], a2: &v1579, a3: v759), (_DWORD)v1579 != 0)
        || (v761 = v1587[0],
            (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v1587[0] + 40LL))(
              a1: v1587[0],
              a2: (__int64)v759 + 20,
              a3: 1),
            *(_DWORD *)(v761 + 16) != 0) )
      {
        v142 = 0;
      }
      else
      {
        v142 = sub_140E45290(a1: v759 + 1, a2: v1587);
      }
      v762 = (void (__fastcall ***)(_QWORD, __int64))v1587[0];
      if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] + 8LL)) == 0 )
        (**v762)(a1: v762, a2: 1);
      if ( v142 == 0 )
        goto LABEL_190;
      v763 = (_QWORD *)a1[4];
      if ( v763 == (_QWORD *)a1[5] )
        break;
      *v763 = v759;
      a1[4] += 8LL;
LABEL_1423:
      if ( ++v758 >= (int)v1602 )
        goto LABEL_190;
    }
    LODWORD(v1598) = v758;
    v764 = (__int64)v763 - a1[3];
    v765 = v764 >> 3;
    v10 = (__int64)a1;
    v766 = (unsigned __int64)(v764 >> 3) >> 1;
    v767 = 0x1FFFFFFFFFFFFFFFLL - v766;
    v768 = (v764 >> 3) + v766;
    v1599 = (v764 >> 3) + 1;
    if ( v768 <= v1599 )
      v768 = v765 + 1;
    if ( v765 > v767 )
      v768 = 0x1FFFFFFFFFFFFFFFLL;
    v769 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v768);
    *(_QWORD *)(v769 + v764) = v759;
    v770 = *(_QWORD **)(v10 + 32);
    sub_141758A00(a1: v769, a2: *(_QWORD *)(v10 + 24), a3: (char *)v763 - *(_QWORD *)(v10 + 24));
    if ( v770 != v763 )
      sub_141758A00(a1: v769 + v764 + 8, a2: v763, a3: *(_QWORD *)(v10 + 32) - (_QWORD)v763);
    v771 = *(_QWORD *)(v10 + 24);
    v32 = (__int64)&unk_141B60B30;
    v772 = v769;
    if ( v771 != 0 )
    {
      v773 = *(_QWORD *)(v10 + 40) - v771;
      if ( v773 == -1 )
        v773 = *(unsigned int *)(v771 - *(unsigned int *)(qword_141ABD470 + 48));
      v1585 = v769;
      if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
        && (v774 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v774) >> 3 > v773)
        && (v775 = *(_QWORD *)(v774 + 8 * v773)) != 0 )
      {
        MEMORY[0x1419475D8](a1: v775 + 32, a2: v771 - *(unsigned int *)(v775 + 120));
        v776 = *(_BYTE *)(v775 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v775 + 64)) != 0;
        v772 = v1585;
        v10 = (__int64)v1603;
        if ( v776 || *(_BYTE *)(v775 + 97) == 0 )
          goto LABEL_1450;
        sub_1412D33C0(a1: v775);
      }
      else
      {
        MEMORY[0x141948990](a1: v771 - *(unsigned int *)(qword_141ABD470 + 48));
        v10 = (__int64)v1603;
      }
      v772 = v1585;
    }
LABEL_1450:
    *(_QWORD *)(v10 + 24) = v772;
    *(_QWORD *)(v10 + 32) = v772 + 8 * v1599;
    *(_QWORD *)(v10 + 40) = v772 + 8 * v768;
    a1 = (_QWORD *)v10;
    LODWORD(v10) = (unsigned __int8)v1604;
    v758 = v1598;
    goto LABEL_1423;
  }
  v597 = 0;
  while ( 1 )
  {
    v32 = (__int64)a1;
    if ( dword_141B60B80 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(a1: &dword_141B60B80);
      if ( dword_141B60B80 == -1 )
      {
        sub_1407E53D0(
          a1: (unsigned int)&unk_141B60B30,
          a2: 1100150566,
          a3: 2048,
          a4: 24,
          a5: 0,
          a6: 1,
          a7: 2048,
          a8: 4096);
        sub_141751048(a1: sub_140FE20E0);
        sub_141750EA0(a1: &dword_141B60B80);
      }
    }
    v679 = (_QWORD *)sub_1407E58C0(a1: &unk_141B60B30, a2: 24);
    *v679 = 0;
    v679[1] = 0;
    *(_QWORD *)((char *)v679 + 13) = 0;
    v1587[0] = v1596;
    _InterlockedIncrement(v1596 + 2);
    v680 = v679 + 2;
    v681 = v1587[0];
    (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)v1587[0] + 40LL))(a1: v1587[0], a2: v679 + 2, a3: 4);
    if ( *(_DWORD *)(v681 + 16) != 0
      || (sub_140814B10(a1: v1587[0], a2: &v1579, a3: v679), (_DWORD)v1579 != 0)
      || (v682 = v1587[0],
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v1587[0] + 40LL))(
            a1: v1587[0],
            a2: (__int64)v679 + 20,
            a3: 1),
          *(_DWORD *)(v682 + 16) != 0) )
    {
      v683 = 0;
    }
    else
    {
      v683 = sub_140E45290(a1: v679 + 1, a2: v1587);
    }
    v684 = (void (__fastcall ***)(_QWORD, __int64))v1587[0];
    if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] + 8LL)) == 0 )
      (**v684)(a1: v684, a2: 1);
    if ( (_BYTE)v683 == 0 )
      break;
    v1598 = (unsigned __int64)v679;
    LODWORD(v1599) = v683;
    v10 = *(_QWORD *)(v32 + 24);
    v685 = *(unsigned __int64 **)(v32 + 32);
    v32 = (__int64)v685 - v10;
    v686 = (unsigned __int64 *)v10;
    if ( (__int64)v685 - v10 > 0 )
    {
      v687 = (unsigned __int64)v32 >> 3;
      v686 = (unsigned __int64 *)v10;
      v688 = (unsigned __int64)v32 >> 3;
      do
      {
        v688 = (unsigned __int64)v688 >> 1;
        if ( *(_DWORD *)(v686[v688] + 16) < *v680 )
        {
          v686 += v688 + 1;
          v688 = v687 + ~v688;
        }
        v687 = v688;
      }
      while ( v688 > 0 );
    }
    if ( v686 == v685 )
    {
      a1 = v1603;
      if ( v685 != (unsigned __int64 *)v1603[5] )
      {
        *v685 = v1598;
        a1[4] += 8LL;
        LODWORD(v10) = (unsigned __int8)v1604;
        v142 = v1599;
        goto LABEL_1254;
      }
      LODWORD(v1585) = v597;
      v703 = v1603;
      v704 = (unsigned __int64)(v32 >> 3) >> 1;
      v705 = 0x1FFFFFFFFFFFFFFFLL - v704;
      v706 = (v32 >> 3) + v704;
      v1582 = (v32 >> 3) + 1;
      if ( v706 <= v1582 )
        v706 = (v32 >> 3) + 1;
      if ( v32 >> 3 > v705 )
        v706 = 0x1FFFFFFFFFFFFFFFLL;
      v707 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v706);
      *(_QWORD *)(v707 + v32) = v1598;
      v10 = v703[4];
      sub_141758A00(a1: v707, a2: v703[3], a3: (char *)v685 - v703[3]);
      v390 = v10 == (_QWORD)v685;
      LODWORD(v10) = (unsigned __int8)v1604;
      if ( !v390 )
      {
        v32 += v707 + 8;
        sub_141758A00(a1: v32, a2: v685, a3: v703[4] - (_QWORD)v685);
      }
      v708 = v703[3];
      if ( v708 != 0 )
      {
        v10 = (__int64)v703;
        v709 = v703[5] - v708;
        if ( v709 == -1 )
          v709 = *(unsigned int *)(v708 - *(unsigned int *)(qword_141ABD470 + 48));
        if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
          && (v710 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v710) >> 3 > v709)
          && (v32 = *(_QWORD *)(v710 + 8 * v709)) != 0 )
        {
          MEMORY[0x1419475D8](a1: v32 + 32, a2: v708 - *(unsigned int *)(v32 + 120));
          v711 = *(_BYTE *)(v32 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v32 + 64)) != 0;
          v703 = (_QWORD *)v10;
          LODWORD(v10) = (unsigned __int8)v1604;
          if ( !v711 && *(_BYTE *)(v32 + 97) != 0 )
            sub_1412D33C0(a1: v32);
        }
        else
        {
          MEMORY[0x141948990](a1: v708 - *(unsigned int *)(qword_141ABD470 + 48));
          v703 = (_QWORD *)v10;
          LODWORD(v10) = (unsigned __int8)v1604;
        }
      }
      v703[3] = v707;
      v703[4] = v707 + 8 * v1582;
      v703[5] = v707 + 8 * v706;
      a1 = v703;
    }
    else
    {
      LODWORD(v1585) = v597;
      v689 = ((__int64)v686 - v10) >> 3;
      if ( *(_DWORD *)(*v686 + 16) == *v680 )
      {
        v32 >>= 3;
        if ( v32 > v689 )
        {
          v690 = *(__int64 **)(v10 + 8 * v689);
          if ( v690 != nullptr )
          {
            sub_140E44A40(a1: v690 + 1);
            v691 = *v690;
            if ( *v690 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v691 - 4)) == 0 )
              sub_1412EC9A0(a1: v691 - 4);
            sub_140FE1F80(a1: v690);
            v10 = v1603[3];
            v685 = (unsigned __int64 *)v1603[4];
            v32 = ((__int64)v685 - v10) >> 3;
          }
        }
        if ( v32 <= v689 )
        {
          v692 = v689 + 1;
          v693 = v689 + 1 - v32;
          if ( v689 + 1 < v32 )
          {
            v1603[4] = v10 + 8 * v692;
          }
          else if ( v689 + 1 > v32 )
          {
            v694 = v1603;
            v695 = (v1603[5] - v10) >> 3;
            if ( v695 >= v692 )
            {
              sub_141758A10(a1: v685, a2: 0, a3: 8 * v693);
              v694[4] = &v685[v693];
              v10 = v694[3];
            }
            else
            {
              v331 = v692 >> 61;
              if ( v692 >> 61 != 0 )
                goto LABEL_3116;
              v696 = v695 + (v695 >> 1);
              if ( v696 <= v692 )
                v696 = v689 + 1;
              if ( v695 > 0x1FFFFFFFFFFFFFFFLL - (v695 >> 1) )
                v696 = 0x1FFFFFFFFFFFFFFFLL;
              v10 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v696);
              sub_141758A10(a1: v10 + 8 * v32, a2: 0, a3: 8 * v693);
              v697 = v1603;
              sub_141758A00(a1: v10, a2: v1603[3], a3: v1603[4] - v1603[3]);
              v698 = v697[3];
              if ( v698 != 0 )
              {
                v699 = v697[5] - v698;
                if ( v699 == -1 )
                  v699 = *(unsigned int *)(v698 - *(unsigned int *)(qword_141ABD470 + 48));
                if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                  && (v700 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v700) >> 3 > v699)
                  && (v32 = *(_QWORD *)(v700 + 8 * v699)) != 0 )
                {
                  MEMORY[0x1419475D8](a1: v32 + 32, a2: v698 - *(unsigned int *)(v32 + 120));
                  v701 = *(_BYTE *)(v32 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v32 + 64)) != 0;
                  v697 = v1603;
                  if ( !v701 && *(_BYTE *)(v32 + 97) != 0 )
                    sub_1412D33C0(a1: v32);
                }
                else
                {
                  MEMORY[0x141948990](a1: v698 - *(unsigned int *)(qword_141ABD470 + 48));
                  v697 = v1603;
                }
              }
              v697[3] = v10;
              v697[4] = v10 + 8 * (v689 + 1);
              v697[5] = v10 + 8 * v696;
            }
          }
        }
        *(_QWORD *)(v10 + 8 * v689) = v1598;
        a1 = v1603;
        LODWORD(v10) = (unsigned __int8)v1604;
      }
      else
      {
        v702 = (char *)(v10 + 8 * v689);
        a1 = v1603;
        if ( v685 == (unsigned __int64 *)v1603[5] )
        {
          v712 = v32 >> 3;
          v713 = v1603;
          v714 = v712 + 1;
          v715 = v712 + (v712 >> 1);
          if ( v715 <= v712 + 1 )
            v715 = v712 + 1;
          if ( v712 > 0x1FFFFFFFFFFFFFFFLL - (v712 >> 1) )
            v715 = 0x1FFFFFFFFFFFFFFFLL;
          v32 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v715);
          *(_QWORD *)(v32 + 8 * v689) = v1598;
          v10 = v713[4];
          sub_141758A00(a1: v32, a2: v713[3], a3: &v702[-v713[3]]);
          v390 = v10 == (_QWORD)v702;
          LODWORD(v10) = (unsigned __int8)v1604;
          if ( !v390 )
            sub_141758A00(a1: v32 + 8 * v689 + 8, a2: v702, a3: v713[4] - (_QWORD)v702);
          v716 = v713[3];
          if ( v716 != 0 )
          {
            v10 = (__int64)v713;
            v717 = v713[5] - v716;
            if ( v717 == -1 )
              v717 = *(unsigned int *)(v716 - *(unsigned int *)(qword_141ABD470 + 48));
            if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
              && (v718 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v718) >> 3 > v717)
              && (v719 = *(_QWORD *)(v718 + 8 * v717)) != 0 )
            {
              MEMORY[0x1419475D8](a1: v719 + 32, a2: v716 - *(unsigned int *)(v719 + 120));
              v720 = *(_BYTE *)(v719 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v719 + 64)) != 0;
              v713 = (_QWORD *)v10;
              LODWORD(v10) = (unsigned __int8)v1604;
              if ( !v720 && *(_BYTE *)(v719 + 97) != 0 )
                sub_1412D33C0(a1: v719);
            }
            else
            {
              MEMORY[0x141948990](a1: v716 - *(unsigned int *)(qword_141ABD470 + 48));
              v713 = (_QWORD *)v10;
              LODWORD(v10) = (unsigned __int8)v1604;
            }
          }
          v713[3] = v32;
          v713[4] = v32 + 8 * v714;
          v713[5] = v32 + 8 * v715;
          a1 = v713;
        }
        else
        {
          LODWORD(v10) = (unsigned __int8)v1604;
          if ( v685 == (unsigned __int64 *)v702 )
          {
            *v685 = v1598;
            a1[4] += 8LL;
          }
          else
          {
            *v685 = *(v685 - 1);
            a1[4] += 8LL;
            sub_141758A00(a1: v702 + 8, a2: v702, a3: (char *)(v685 - 1) - v702);
            *(_QWORD *)v702 = v1598;
          }
        }
      }
    }
    v142 = v1599;
    v597 = v1585;
LABEL_1254:
    if ( ++v597 >= (int)v1602 )
      goto LABEL_190;
  }
  v142 = 0;
  LODWORD(v10) = (unsigned __int8)v1604;
  a1 = (_QWORD *)v32;
LABEL_190:
  v143 = v1596;
  if ( v1596 != nullptr && _InterlockedDecrement(v1596 + 2) == 0 )
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v143)(a1: v143, a2: 1);
  v85 = v1605;
  if ( v142 == 0 )
    goto LABEL_2936;
LABEL_194:
  if ( (v85 & (unsigned __int8)(v10 & v1584)) == 0 )
    goto LABEL_324;
  v144 = *((_DWORD *)a1 + 92);
  v32 = (__int64)&v1595;
  sub_14080D0E0(a1: &v1595, a2: 0x1418E2C24LL);
  LODWORD(v1599) = v144;
  LODWORD(v1593) = v144;
  v1594 = 47;
  sub_1408085A0(a1: &v1579, a2: &v1594);
  sub_1408085A0(a1: &v1602, a2: &v1593);
  v1600 = nullptr;
  v145 = v1602;
  if ( v1602 != nullptr )
  {
    _InterlockedIncrement(v1602 - 1);
    v1600 = v145;
    v146 = *v145;
  }
  else
  {
    v146 = 0;
  }
  v193 = v146 + 1;
  v194 = sub_1412EC810(a1: 264, a2: (unsigned int)(v146 + 1));
  v195 = (volatile signed __int32 *)v194;
  *(_DWORD *)v194 = 0;
  v196 = 0;
  if ( v146 + 1 <= 0 )
    v193 = 0;
  *(_DWORD *)(v194 + 4) = v193;
  v197 = v194 + 8;
  *(_BYTE *)(v194 + 8) = 0;
  if ( v146 <= 0 )
  {
    v199 = (_BYTE *)(v194 + 8);
    if ( v146 == 0 )
      goto LABEL_296;
  }
  else
  {
    v198 = 0x1419435F1LL;
    if ( v1600 != nullptr )
      v198 = (__int64)(v1600 + 1);
    sub_141758A00(a1: v194 + 8, a2: v198, a3: (unsigned int)v146);
    v199 = (_BYTE *)(v197 + (unsigned int)v146);
LABEL_296:
    *v199 = 0;
    v196 = v146;
  }
  v200 = (volatile signed __int32 *)(v194 + 4);
  *(_WORD *)(v197 + v196) = 95;
  v201 = v1600 - 1;
  if ( v1600 != nullptr && _InterlockedDecrement(v201) == 0 )
    sub_1412EC9A0(a1: v201);
  v1600 = nullptr;
  _InterlockedIncrement(v195);
  v1600 = v200;
  sub_140809550(a1: &v1600, a2: v1587, a3: &v1579);
  v1583 = 0;
  v202 = v1587[0];
  if ( v1587[0] != 0 )
  {
    _InterlockedIncrement((volatile signed __int32 *)(v1587[0] - 4LL));
    v203 = v1587[0];
    v1583 = v202;
    if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] - 4LL)) == 0 )
      sub_1412EC9A0(a1: v203 - 4);
  }
  v204 = v1600;
  v205 = v1603;
  if ( v1600 != nullptr && _InterlockedDecrement(v1600 - 1) == 0 )
    sub_1412EC9A0(a1: v204 - 1);
  v206 = v1602;
  if ( v1602 != nullptr && _InterlockedDecrement(v1602 - 1) == 0 )
    sub_1412EC9A0(a1: v206 - 1);
  v207 = v1579;
  if ( v1579 != nullptr && _InterlockedDecrement(v1579 - 1) == 0 )
    sub_1412EC9A0(a1: v207 - 1);
  v1587[0] = 0x80100004E554C4CLL;
  LOBYTE(v1553) = 0;
  sub_1407D0F70(
    a1: (unsigned int)v1587,
    a2: (unsigned int)&v1596,
    a3: a2,
    a4: (unsigned int)&v1583,
    a5: (__int64)&v1595,
    a6: 0,
    a7: 0,
    v1553);
  v208 = v1583;
  if ( v1583 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1583 - 4)) == 0 )
    sub_1412EC9A0(a1: v208 - 4);
  v209 = v1596;
  if ( v1596 == nullptr )
    goto LABEL_2936;
  v210 = v205[25] != v205[24];
  LODWORD(v1600) = 0;
  (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **, __int64))(*(_QWORD *)v1596 + 40LL))(
    a1: v1596,
    a2: &v1600,
    a3: 4);
  if ( *((_DWORD *)v209 + 4) != 0 )
  {
LABEL_319:
    LODWORD(v32) = 0;
    goto LABEL_320;
  }
  if ( v1601 != 0 )
  {
    LOBYTE(v32) = 1;
    if ( (int)v1600 <= 0 )
      goto LABEL_320;
    v285 = 0;
    v32 = (__int64)&v1587[2];
    while ( 1 )
    {
      memset(v1587, 0, 28);
      WORD2(v1587[3]) = -1;
      v1579 = v1596;
      if ( v1596 != nullptr )
        _InterlockedIncrement(v1596 + 2);
      v286 = sub_140E498B0(a1: v1587, a2: &v1579, a3: (unsigned int)v1599);
      v287 = v1579;
      if ( v1579 != nullptr && _InterlockedDecrement(v1579 + 2) == 0 )
        (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v287)(a1: v287, a2: 1);
      if ( v286 == 0 )
        break;
      sub_141459800(a1: v1587);
      sub_140E44A40(a1: &v1587[2]);
      v288 = v1587[1];
      if ( v1587[1] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[1] - 4LL)) == 0 )
        sub_1412EC9A0(a1: v288 - 4);
      v289 = v1587[0];
      if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] - 4LL)) == 0 )
        sub_1412EC9A0(a1: v289 - 4);
      if ( ++v285 >= (int)v1600 )
      {
        LOBYTE(v32) = 1;
        goto LABEL_320;
      }
    }
    sub_140E44A40(a1: &v1587[2]);
    v958 = v1587[1];
    if ( v1587[1] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[1] - 4LL)) == 0 )
      sub_1412EC9A0(a1: v958 - 4);
    v959 = v1587[0];
    if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] - 4LL)) == 0 )
      sub_1412EC9A0(a1: v959 - 4);
    goto LABEL_319;
  }
  v460 = (int)v1600;
  if ( v210 )
  {
    v461 = v205[24];
    v462 = (v205[25] - v461) >> 3;
    v463 = v462 + (int)v1600;
    v464 = (v205[26] - v461) >> 3;
    if ( v464 < v463 )
    {
      if ( v463 >> 61 == 0 )
      {
        v32 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v463);
        sub_141758A00(a1: v32, a2: v205[24], a3: v205[25] - v205[24]);
        if ( v205[24] != 0 )
          sub_1407E4890(a1: qword_141ABD470);
        v205[24] = v32;
        v205[25] = v32 + 8 * v462;
        v465 = v32 + 8 * v463;
        goto LABEL_1413;
      }
LABEL_3118:
      sub_1400526C0(a1: v464);
    }
  }
  else
  {
    v32 = v205[24];
    v464 = (v205[26] - v32) >> 3;
    if ( v464 < (int)v1600 )
    {
      if ( (int)v1600 < 0 )
        goto LABEL_3118;
      v753 = v205[25];
      v754 = sub_1407E4490(a1: qword_141ABD470, a2: 8LL * (int)v1600);
      sub_141758A00(a1: v754, a2: v205[24], a3: v205[25] - v205[24]);
      if ( v205[24] != 0 )
        sub_1407E4890(a1: qword_141ABD470);
      v205[24] = v754;
      v205[25] = v754 + v753 - v32;
      v465 = v754 + 8 * v460;
LABEL_1413:
      v205[26] = v465;
    }
  }
  if ( (int)v1600 <= 0 )
  {
    LOBYTE(v32) = 1;
    LODWORD(v10) = (unsigned __int8)v1604;
    goto LABEL_320;
  }
  LODWORD(v10) = (unsigned __int8)v1604;
  if ( !v210 )
  {
    v960 = 0;
    do
    {
      v961 = sub_141750CC0(a1: 32);
      *(_QWORD *)v961 = 0;
      *(_QWORD *)(v961 + 8) = 0;
      *(_QWORD *)(v961 + 16) = 0;
      *(_WORD *)(v961 + 28) = -1;
      *(_DWORD *)(v961 + 24) = 0;
      v1587[0] = v1596;
      if ( v1596 != nullptr )
        _InterlockedIncrement(v1596 + 2);
      v962 = v10;
      LODWORD(v32) = sub_140E498B0(a1: v961, a2: v1587, a3: (unsigned int)v1599);
      v963 = (void (__fastcall ***)(_QWORD, __int64))v1587[0];
      if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] + 8LL)) == 0 )
        (**v963)(a1: v963, a2: 1);
      if ( (_BYTE)v32 == 0 )
        break;
      v10 = (__int64)v1603;
      v964 = (__int64 *)v1603[25];
      if ( v964 == (__int64 *)v1603[26] )
      {
        LODWORD(v1598) = v32;
        v965 = (__int64)v964 - v1603[24];
        v966 = v965 >> 3;
        v967 = (unsigned __int64)(v965 >> 3) >> 1;
        v968 = 0x1FFFFFFFFFFFFFFFLL - v967;
        v32 = (v965 >> 3) + v967;
        v1584 = (v965 >> 3) + 1;
        if ( v32 <= v1584 )
          v32 = v966 + 1;
        if ( v966 > v968 )
          v32 = 0x1FFFFFFFFFFFFFFFLL;
        v969 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v32);
        *(_QWORD *)(v969 + v965) = v961;
        v970 = *(__int64 **)(v10 + 200);
        sub_141758A00(a1: v969, a2: *(_QWORD *)(v10 + 192), a3: (char *)v964 - *(_QWORD *)(v10 + 192));
        if ( v970 != v964 )
          sub_141758A00(a1: v969 + v965 + 8, a2: v964, a3: *(_QWORD *)(v10 + 200) - (_QWORD)v964);
        v971 = v969;
        v972 = *(_QWORD *)(v10 + 192);
        if ( v972 != 0 )
        {
          v973 = *(_QWORD *)(v10 + 208) - v972;
          if ( v973 == -1 )
            v973 = *(unsigned int *)(v972 - *(unsigned int *)(qword_141ABD470 + 48));
          if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
            && (v974 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v974) >> 3 > v973)
            && (v975 = *(_QWORD *)(v974 + 8 * v973)) != 0 )
          {
            MEMORY[0x1419475D8](a1: v975 + 32, a2: v972 - *(unsigned int *)(v975 + 120));
            v976 = *(_BYTE *)(v975 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v975 + 64)) != 0;
            v10 = (__int64)v1603;
            if ( !v976 && *(_BYTE *)(v975 + 97) != 0 )
              sub_1412D33C0(a1: v975);
          }
          else
          {
            MEMORY[0x141948990](a1: v972 - *(unsigned int *)(qword_141ABD470 + 48));
            v10 = (__int64)v1603;
          }
        }
        *(_QWORD *)(v10 + 192) = v971;
        *(_QWORD *)(v10 + 200) = v971 + 8 * v1584;
        *(_QWORD *)(v10 + 208) = v971 + 8 * v32;
        LODWORD(v10) = (unsigned __int8)v1604;
        LODWORD(v32) = v1598;
      }
      else
      {
        *v964 = v961;
        *(_QWORD *)(v10 + 200) += 8LL;
        LODWORD(v10) = v962;
      }
      ++v960;
    }
    while ( v960 < (int)v1600 );
    goto LABEL_320;
  }
  v755 = 0;
  while ( 2 )
  {
    v876 = sub_141750CC0(a1: 32);
    *(_QWORD *)v876 = 0;
    *(_QWORD *)(v876 + 8) = 0;
    *(_QWORD *)(v876 + 16) = 0;
    *(_WORD *)(v876 + 28) = -1;
    *(_DWORD *)(v876 + 24) = 0;
    v1587[0] = v1596;
    if ( v1596 != nullptr )
      _InterlockedIncrement(v1596 + 2);
    v877 = sub_140E498B0(a1: v876, a2: v1587, a3: (unsigned int)v1599);
    v878 = (void (__fastcall ***)(_QWORD, __int64))v1587[0];
    v879 = v1603;
    if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] + 8LL)) == 0 )
      (**v878)(a1: v878, a2: 1);
    if ( (_BYTE)v877 != 0 )
    {
      LODWORD(v1598) = v877;
      v880 = v879[24];
      v881 = (__int64 *)v879[25];
      v882 = (__int64)v881 - v880;
      v883 = (__int64 *)v880;
      if ( (__int64)v881 - v880 > 0 )
      {
        v884 = (unsigned __int64)v882 >> 3;
        v883 = (__int64 *)v879[24];
        v885 = (unsigned __int64)v882 >> 3;
        do
        {
          v885 = (unsigned __int64)v885 >> 1;
          if ( *(_DWORD *)(v883[v885] + 24) < *(_DWORD *)(v876 + 24) )
          {
            v883 += v885 + 1;
            v885 = v884 + ~v885;
          }
          v884 = v885;
        }
        while ( v885 > 0 );
      }
      LODWORD(v1584) = v755;
      if ( v883 == v881 )
      {
        v902 = v1603;
        if ( v881 != (__int64 *)v1603[26] )
        {
          *v881 = v876;
          v902[25] += 8LL;
          goto LABEL_1693;
        }
        v905 = (unsigned __int64)(v882 >> 3) >> 1;
        v906 = 0x1FFFFFFFFFFFFFFFLL - v905;
        v907 = (v882 >> 3) + v905;
        v1585 = (v882 >> 3) + 1;
        if ( v907 <= v1585 )
          v907 = (v882 >> 3) + 1;
        if ( v882 >> 3 > v906 )
          v907 = 0x1FFFFFFFFFFFFFFFLL;
        v908 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v907);
        *(_QWORD *)(v908 + v882) = v876;
        v909 = v908;
        v910 = (__int64 *)v902[25];
        sub_141758A00(a1: v908, a2: v902[24], a3: (char *)v881 - v902[24]);
        if ( v910 != v881 )
          sub_141758A00(a1: v909 + v882 + 8, a2: v881, a3: v902[25] - (_QWORD)v881);
        v911 = v902[24];
        LODWORD(v10) = (unsigned __int8)v1604;
        LODWORD(v32) = v1598;
        if ( v911 != 0 )
        {
          v912 = v902[26] - v911;
          if ( v912 == -1 )
            v912 = *(unsigned int *)(v911 - *(unsigned int *)(qword_141ABD470 + 48));
          if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
            && (v913 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v913) >> 3 > v912)
            && (v914 = *(_QWORD *)(v913 + 8 * v912)) != 0 )
          {
            MEMORY[0x1419475D8](a1: v914 + 32, a2: v911 - *(unsigned int *)(v914 + 120));
            v915 = *(_BYTE *)(v914 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v914 + 64)) != 0;
            if ( !v915 && *(_BYTE *)(v914 + 97) != 0 )
              sub_1412D33C0(a1: v914);
          }
          else
          {
            MEMORY[0x141948990](a1: v911 - *(unsigned int *)(qword_141ABD470 + 48));
          }
        }
        v902[24] = v909;
        v902[25] = v909 + 8 * v1585;
        v902[26] = v909 + 8 * v907;
      }
      else
      {
        v886 = ((__int64)v883 - v880) >> 3;
        if ( *(_DWORD *)(*v883 + 24) == *(_DWORD *)(v876 + 24) )
        {
          v887 = v882 >> 3;
          if ( v887 > v886 )
          {
            v888 = *(__int64 **)(v880 + 8 * v886);
            if ( v888 != nullptr )
            {
              sub_140E44A40(a1: v888 + 2);
              v889 = v888[1];
              if ( v889 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v889 - 4)) == 0 )
                sub_1412EC9A0(a1: v889 - 4);
              v890 = *v888;
              v891 = v1603;
              if ( *v888 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v890 - 4)) == 0 )
                sub_1412EC9A0(a1: v890 - 4);
              sub_141750CFC(a1: v888);
              v880 = v891[24];
              v881 = (__int64 *)v891[25];
              v887 = ((__int64)v881 - v880) >> 3;
            }
          }
          if ( v887 <= v886 )
          {
            v892 = v886 + 1;
            v893 = v886 + 1 - v887;
            if ( v886 + 1 < v887 )
            {
              v1603[25] = v880 + 8 * v892;
            }
            else if ( v886 + 1 > v887 )
            {
              v894 = (v1603[26] - v880) >> 3;
              if ( v894 >= v892 )
              {
                v926 = v1603;
                sub_141758A10(a1: v881, a2: 0, a3: 8 * v893);
                v926[25] = &v881[v893];
                v880 = v926[24];
              }
              else
              {
                v464 = v892 >> 61;
                if ( v892 >> 61 != 0 )
                  goto LABEL_3118;
                v895 = v894 + (v894 >> 1);
                v1585 = v886 + 1;
                if ( v895 <= v892 )
                  v895 = v886 + 1;
                if ( v894 > 0x1FFFFFFFFFFFFFFFLL - (v894 >> 1) )
                  v895 = 0x1FFFFFFFFFFFFFFFLL;
                v880 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v895);
                sub_141758A10(a1: v880 + 8 * v887, a2: 0, a3: 8 * v893);
                v896 = v1603;
                sub_141758A00(a1: v880, a2: v1603[24], a3: v1603[25] - v1603[24]);
                v897 = v896[24];
                if ( v897 != 0 )
                {
                  v898 = v896[26] - v897;
                  if ( v898 == -1 )
                    v898 = *(unsigned int *)(v897 - *(unsigned int *)(qword_141ABD470 + 48));
                  if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                    && (v899 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v899) >> 3 > v898)
                    && (v900 = *(_QWORD *)(v899 + 8 * v898)) != 0 )
                  {
                    MEMORY[0x1419475D8](a1: v900 + 32, a2: v897 - *(unsigned int *)(v900 + 120));
                    v901 = *(_BYTE *)(v900 + 72) != 0
                        && _InterlockedDecrement((volatile signed __int32 *)(v900 + 64)) != 0;
                    v896 = v1603;
                    if ( !v901 && *(_BYTE *)(v900 + 97) != 0 )
                      sub_1412D33C0(a1: v900);
                  }
                  else
                  {
                    MEMORY[0x141948990](a1: v897 - *(unsigned int *)(qword_141ABD470 + 48));
                  }
                }
                v896[24] = v880;
                v896[25] = v880 + 8 * v1585;
                v896[26] = v880 + 8 * v895;
              }
            }
          }
          *(_QWORD *)(v880 + 8 * v886) = v876;
        }
        else
        {
          v903 = (__int64 *)(v880 + 8 * v886);
          v904 = v1603;
          if ( v881 == (__int64 *)v1603[26] )
          {
            v916 = v882 >> 3;
            v917 = v916 + 1;
            v918 = v916 + (v916 >> 1);
            if ( v918 <= v916 + 1 )
              v918 = v916 + 1;
            if ( v916 > 0x1FFFFFFFFFFFFFFFLL - (v916 >> 1) )
              v918 = 0x1FFFFFFFFFFFFFFFLL;
            v919 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v918);
            *(_QWORD *)(v919 + 8 * v886) = v876;
            v920 = (__int64 *)v904[25];
            sub_141758A00(a1: v919, a2: v904[24], a3: (char *)v903 - v904[24]);
            if ( v920 != v903 )
              sub_141758A00(a1: v919 + 8 * v886 + 8, a2: v903, a3: v904[25] - (_QWORD)v903);
            v921 = v904[24];
            if ( v921 != 0 )
            {
              v922 = v904[26] - v921;
              if ( v922 == -1 )
                v922 = *(unsigned int *)(v921 - *(unsigned int *)(qword_141ABD470 + 48));
              if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                && (v923 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v923) >> 3 > v922)
                && (v924 = *(_QWORD *)(v923 + 8 * v922)) != 0 )
              {
                MEMORY[0x1419475D8](a1: v924 + 32, a2: v921 - *(unsigned int *)(v924 + 120));
                v925 = *(_BYTE *)(v924 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v924 + 64)) != 0;
                v904 = v1603;
                if ( !v925 && *(_BYTE *)(v924 + 97) != 0 )
                  sub_1412D33C0(a1: v924);
              }
              else
              {
                MEMORY[0x141948990](a1: v921 - *(unsigned int *)(qword_141ABD470 + 48));
                v904 = v1603;
              }
            }
            v904[24] = v919;
            v904[25] = v919 + 8 * v917;
            v904[26] = v919 + 8 * v918;
          }
          else if ( v881 == v903 )
          {
            *v881 = v876;
            v1603[25] += 8LL;
          }
          else
          {
            *v881 = *(v881 - 1);
            v1603[25] += 8LL;
            sub_141758A00(a1: v903 + 1, a2: v880 + 8 * v886, a3: (char *)(v881 - 1) - (char *)v903);
            *v903 = v876;
          }
        }
LABEL_1693:
        LODWORD(v10) = (unsigned __int8)v1604;
        LODWORD(v32) = v1598;
      }
      v755 = v1584 + 1;
      if ( (int)v1584 + 1 >= (int)v1600 )
        goto LABEL_320;
      continue;
    }
    break;
  }
  LODWORD(v32) = 0;
  LODWORD(v10) = (unsigned __int8)v1604;
LABEL_320:
  v211 = v1596;
  if ( v1596 != nullptr && _InterlockedDecrement(v1596 + 2) == 0 )
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v211)(a1: v211, a2: 1);
  v85 = v1605;
  a1 = v1603;
  if ( (_BYTE)v32 == 0 )
    goto LABEL_2936;
LABEL_324:
  if ( (v85 & (unsigned __int8)(v10 & v1555)) == 0 )
  {
    LOBYTE(v32) = 1;
    goto LABEL_447;
  }
  v212 = *((_DWORD *)a1 + 92);
  sub_14080D0E0(a1: &v1595, a2: 0x1418E2C24LL);
  LODWORD(v1599) = v212;
  LODWORD(v1593) = v212;
  v1594 = 5;
  sub_1408085A0(a1: &v1579, a2: &v1594);
  sub_1408085A0(a1: &v1602, a2: &v1593);
  v1600 = nullptr;
  v213 = v1602;
  if ( v1602 != nullptr )
  {
    _InterlockedIncrement(v1602 - 1);
    v1600 = v213;
    v214 = *v213;
  }
  else
  {
    v214 = 0;
  }
  v265 = v214 + 1;
  v266 = sub_1412EC810(a1: 264, a2: (unsigned int)(v214 + 1));
  v32 = v266;
  *(_DWORD *)v266 = 0;
  v267 = 0;
  if ( v214 + 1 <= 0 )
    v265 = 0;
  *(_DWORD *)(v266 + 4) = v265;
  v268 = v266 + 8;
  *(_BYTE *)(v266 + 8) = 0;
  if ( v214 <= 0 )
  {
    v270 = (_BYTE *)(v266 + 8);
    if ( v214 == 0 )
      goto LABEL_419;
  }
  else
  {
    v269 = 0x1419435F1LL;
    if ( v1600 != nullptr )
      v269 = (__int64)(v1600 + 1);
    sub_141758A00(a1: v266 + 8, a2: v269, a3: (unsigned int)v214);
    v270 = (_BYTE *)(v268 + (unsigned int)v214);
LABEL_419:
    *v270 = 0;
    v267 = v214;
  }
  v271 = (volatile signed __int32 *)(v266 + 4);
  *(_WORD *)(v268 + v267) = 95;
  v272 = v1600 - 1;
  if ( v1600 != nullptr && _InterlockedDecrement(v272) == 0 )
    sub_1412EC9A0(a1: v272);
  v1600 = nullptr;
  _InterlockedIncrement((volatile signed __int32 *)v32);
  v1600 = v271;
  sub_140809550(a1: &v1600, a2: v1587, a3: &v1579);
  v1583 = 0;
  v273 = v1587[0];
  if ( v1587[0] != 0 )
  {
    _InterlockedIncrement((volatile signed __int32 *)(v1587[0] - 4LL));
    v274 = v1587[0];
    v1583 = v273;
    if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] - 4LL)) == 0 )
      sub_1412EC9A0(a1: v274 - 4);
  }
  v275 = v1600;
  if ( v1600 != nullptr && _InterlockedDecrement(v1600 - 1) == 0 )
    sub_1412EC9A0(a1: v275 - 1);
  v276 = v1602;
  if ( v1602 != nullptr && _InterlockedDecrement(v1602 - 1) == 0 )
    sub_1412EC9A0(a1: v276 - 1);
  v277 = v1579;
  if ( v1579 != nullptr && _InterlockedDecrement(v1579 - 1) == 0 )
    sub_1412EC9A0(a1: v277 - 1);
  v1587[0] = 0x80100004E554C4CLL;
  LOBYTE(v1553) = 0;
  sub_1407D0F70(
    a1: (unsigned int)v1587,
    a2: (unsigned int)&v1596,
    a3: a2,
    a4: (unsigned int)&v1583,
    a5: (__int64)&v1595,
    a6: 0,
    a7: 0,
    v1553);
  v278 = v1583;
  if ( v1583 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1583 - 4)) == 0 )
    sub_1412EC9A0(a1: v278 - 4);
  v279 = v1596;
  a1 = v1603;
  if ( v1596 == nullptr )
    goto LABEL_2936;
  v280 = v1603[13] != v1603[12];
  LODWORD(v1600) = 0;
  (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **, __int64))(*(_QWORD *)v1596 + 40LL))(
    a1: v1596,
    a2: &v1600,
    a3: 4);
  if ( *((_DWORD *)v279 + 4) != 0 )
  {
LABEL_442:
    LODWORD(v32) = 0;
    goto LABEL_443;
  }
  if ( v1601 == 0 )
  {
    v668 = (int)v1600;
    v669 = v280;
    if ( v280 )
    {
      v670 = a1[12];
      v671 = (a1[13] - v670) >> 3;
      v672 = v671 + (int)v1600;
      v673 = (a1[14] - v670) >> 3;
      if ( v673 < v672 )
      {
        if ( v672 >> 61 == 0 )
        {
          v32 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v672);
          sub_141758A00(a1: v32, a2: a1[12], a3: a1[13] - a1[12]);
          if ( a1[12] != 0 )
            sub_1407E4890(a1: qword_141ABD470);
          a1[12] = v32;
          a1[13] = v32 + 8 * v671;
          a1[14] = v32 + 8 * v672;
          goto LABEL_1856;
        }
LABEL_3120:
        sub_1400526C0(a1: v673);
      }
    }
    else
    {
      v32 = a1[12];
      v673 = (a1[14] - v32) >> 3;
      if ( v673 < (int)v1600 )
      {
        if ( (int)v1600 >= 0 )
        {
          v954 = a1[13];
          v955 = a1;
          v956 = sub_1407E4490(a1: qword_141ABD470, a2: 8LL * (int)v1600);
          sub_141758A00(a1: v956, a2: v955[12], a3: v955[13] - v955[12]);
          if ( v955[12] != 0 )
            sub_1407E4890(a1: qword_141ABD470);
          v955[12] = v956;
          v955[13] = v956 + v954 - v32;
          v955[14] = v956 + 8 * v668;
          a1 = v955;
          goto LABEL_1856;
        }
        goto LABEL_3120;
      }
    }
LABEL_1856:
    if ( (int)v1600 <= 0 )
    {
      LOBYTE(v32) = 1;
      goto LABEL_443;
    }
    if ( !v669 )
    {
      v1068 = 0;
      do
      {
        if ( dword_141B60A78 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                         + 4LL) )
        {
          sub_141750E08(a1: &dword_141B60A78);
          if ( dword_141B60A78 == -1 )
          {
            sub_1407E53D0(
              a1: (unsigned int)&unk_141B60A28,
              a2: 1100150599,
              a3: 16,
              a4: 56,
              a5: 0,
              a6: 1,
              a7: 16,
              a8: 4096);
            sub_141751048(a1: sub_140FE1C90);
            sub_141750EA0(a1: &dword_141B60A78);
          }
        }
        v1069 = sub_1407E58C0(a1: &unk_141B60A28, a2: 56);
        *(_QWORD *)v1069 = 0;
        *(_QWORD *)(v1069 + 8) = 0;
        *(_QWORD *)(v1069 + 16) = 0;
        *(_QWORD *)(v1069 + 24) = 0;
        *(_QWORD *)(v1069 + 32) = 0;
        *(_QWORD *)(v1069 + 40) = 0;
        *(_DWORD *)(v1069 + 48) = 0;
        *(_WORD *)(v1069 + 52) = -1;
        *(_BYTE *)(v1069 + 54) = -1;
        v1587[0] = v1596;
        if ( v1596 != nullptr )
          _InterlockedIncrement(v1596 + 2);
        LODWORD(v32) = sub_140ED71C0(a1: v1069, a2: v1587, a3: (unsigned int)v1599);
        v1070 = (void (__fastcall ***)(_QWORD, __int64))v1587[0];
        if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] + 8LL)) == 0 )
          (**v1070)(a1: v1070, a2: 1);
        if ( (_BYTE)v32 == 0 )
          break;
        v1071 = (__int64 *)a1[13];
        if ( v1071 == (__int64 *)a1[14] )
        {
          LODWORD(v1584) = v1068;
          v10 = (__int64)a1;
          v1072 = (__int64)v1071 - a1[12];
          v1073 = (unsigned __int64)(v1072 >> 3) >> 1;
          v1074 = 0x1FFFFFFFFFFFFFFFLL - v1073;
          v1075 = (v1072 >> 3) + v1073;
          v1598 = (v1072 >> 3) + 1;
          if ( v1075 <= v1598 )
            v1075 = (v1072 >> 3) + 1;
          if ( v1072 >> 3 > v1074 )
            v1075 = 0x1FFFFFFFFFFFFFFFLL;
          v1076 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v1075);
          *(_QWORD *)(v1076 + v1072) = v1069;
          v1077 = *(__int64 **)(v10 + 104);
          sub_141758A00(a1: v1076, a2: *(_QWORD *)(v10 + 96), a3: (char *)v1071 - *(_QWORD *)(v10 + 96));
          if ( v1077 != v1071 )
            sub_141758A00(a1: v1076 + v1072 + 8, a2: v1071, a3: *(_QWORD *)(v10 + 104) - (_QWORD)v1071);
          v1078 = v1076;
          v1079 = *(_QWORD *)(v10 + 96);
          v1068 = v1584;
          if ( v1079 != 0 )
          {
            v1080 = *(_QWORD *)(v10 + 112) - v1079;
            if ( v1080 == -1 )
              v1080 = *(unsigned int *)(v1079 - *(unsigned int *)(qword_141ABD470 + 48));
            if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
              && (v1081 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v1081) >> 3 > v1080)
              && (v1082 = *(_QWORD *)(v1081 + 8 * v1080)) != 0 )
            {
              MEMORY[0x1419475D8](a1: v1082 + 32, a2: v1079 - *(unsigned int *)(v1082 + 120));
              v1083 = *(_BYTE *)(v1082 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1082 + 64)) != 0;
              v10 = (__int64)v1603;
              if ( !v1083 && *(_BYTE *)(v1082 + 97) != 0 )
                sub_1412D33C0(a1: v1082);
            }
            else
            {
              MEMORY[0x141948990](a1: v1079 - *(unsigned int *)(qword_141ABD470 + 48));
              v10 = (__int64)v1603;
            }
          }
          *(_QWORD *)(v10 + 96) = v1078;
          *(_QWORD *)(v10 + 104) = v1078 + 8 * v1598;
          *(_QWORD *)(v10 + 112) = v1078 + 8 * v1075;
          a1 = (_QWORD *)v10;
          LODWORD(v10) = (unsigned __int8)v1604;
        }
        else
        {
          *v1071 = v1069;
          a1[13] += 8LL;
        }
        ++v1068;
      }
      while ( v1068 < (int)v1600 );
      goto LABEL_443;
    }
    v957 = 0;
    while ( 1 )
    {
      if ( dword_141B60A78 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(a1: &dword_141B60A78);
        if ( dword_141B60A78 == -1 )
        {
          sub_1407E53D0(
            a1: (unsigned int)&unk_141B60A28,
            a2: 1100150599,
            a3: 16,
            a4: 56,
            a5: 0,
            a6: 1,
            a7: 16,
            a8: 4096);
          sub_141751048(a1: sub_140FE1C90);
          sub_141750EA0(a1: &dword_141B60A78);
        }
      }
      v987 = sub_1407E58C0(a1: &unk_141B60A28, a2: 56);
      *(_QWORD *)v987 = 0;
      *(_QWORD *)(v987 + 8) = 0;
      *(_QWORD *)(v987 + 16) = 0;
      *(_QWORD *)(v987 + 24) = 0;
      *(_QWORD *)(v987 + 32) = 0;
      *(_QWORD *)(v987 + 40) = 0;
      *(_DWORD *)(v987 + 48) = 0;
      *(_WORD *)(v987 + 52) = -1;
      *(_BYTE *)(v987 + 54) = -1;
      v1587[0] = v1596;
      if ( v1596 != nullptr )
        _InterlockedIncrement(v1596 + 2);
      LODWORD(v32) = sub_140ED71C0(a1: v987, a2: v1587, a3: (unsigned int)v1599);
      v988 = (void (__fastcall ***)(_QWORD, __int64))v1587[0];
      if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] + 8LL)) == 0 )
        (**v988)(a1: v988, a2: 1);
      if ( (_BYTE)v32 == 0 )
      {
        LODWORD(v32) = 0;
        LODWORD(v10) = (unsigned __int8)v1604;
        goto LABEL_443;
      }
      LODWORD(v1598) = v957;
      v989 = a1;
      v990 = a1[12];
      v991 = (__int64 *)v989[13];
      v992 = (__int64)v991 - v990;
      v993 = (__int64 *)v990;
      if ( (__int64)v991 - v990 > 0 )
      {
        v994 = (unsigned __int64)v992 >> 3;
        v993 = (__int64 *)v990;
        v995 = (unsigned __int64)v992 >> 3;
        do
        {
          v995 = (unsigned __int64)v995 >> 1;
          if ( *(_DWORD *)(v993[v995] + 48) < *(_DWORD *)(v987 + 48) )
          {
            v993 += v995 + 1;
            v995 = v994 + ~v995;
          }
          v994 = v995;
        }
        while ( v995 > 0 );
      }
      if ( v993 == v991 )
        break;
      v996 = ((__int64)v993 - v990) >> 3;
      if ( *(_DWORD *)(*v993 + 48) == *(_DWORD *)(v987 + 48) )
      {
        v997 = v992 >> 3;
        if ( v997 > v996 )
        {
          v998 = *(__int64 **)(v990 + 8 * v996);
          if ( v998 != nullptr )
          {
            sub_140E44A40(a1: v998 + 5);
            v999 = v998[4];
            if ( v999 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v999 - 4)) == 0 )
              sub_1412EC9A0(a1: v999 - 4);
            v1000 = v998[3];
            v1001 = v1603;
            if ( v1000 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1000 - 4)) == 0 )
              sub_1412EC9A0(a1: v1000 - 4);
            v1002 = v998[2];
            if ( v1002 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1002 - 4)) == 0 )
              sub_1412EC9A0(a1: v1002 - 4);
            v1003 = v998[1];
            if ( v1003 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1003 - 4)) == 0 )
              sub_1412EC9A0(a1: v1003 - 4);
            v1004 = *v998;
            if ( *v998 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1004 - 4)) == 0 )
              sub_1412EC9A0(a1: v1004 - 4);
            sub_140FE1B30(a1: v998);
            v990 = v1001[12];
            v991 = (__int64 *)v1001[13];
            v997 = ((__int64)v991 - v990) >> 3;
          }
        }
        if ( v997 <= v996 )
        {
          v1005 = v996 + 1;
          v1006 = v996 + 1 - v997;
          if ( v996 + 1 < v997 )
          {
            v1603[13] = v990 + 8 * v1005;
          }
          else if ( v996 + 1 > v997 )
          {
            v1007 = (v1603[14] - v990) >> 3;
            if ( v1007 >= v1005 )
            {
              v1038 = &v991[v1006];
              v1039 = v1603;
              sub_141758A10(a1: v991, a2: 0, a3: 8 * v1006);
              v1039[13] = v1038;
              v990 = v1039[12];
            }
            else
            {
              v1584 = v996 + 1 - v997;
              v673 = v1005 >> 61;
              if ( v1005 >> 61 != 0 )
                goto LABEL_3120;
              v1008 = v1007 + (v1007 >> 1);
              if ( v1008 <= v1005 )
                v1008 = v996 + 1;
              if ( v1007 > 0x1FFFFFFFFFFFFFFFLL - (v1007 >> 1) )
                v1008 = 0x1FFFFFFFFFFFFFFFLL;
              v990 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v1008);
              sub_141758A10(a1: v990 + 8 * v997, a2: 0, a3: 8 * v1584);
              v1009 = v1603;
              sub_141758A00(a1: v990, a2: v1603[12], a3: v1603[13] - v1603[12]);
              v1010 = v1009[12];
              if ( v1010 != 0 )
              {
                v1011 = v1009[14] - v1010;
                if ( v1011 == -1 )
                  v1011 = *(unsigned int *)(v1010 - *(unsigned int *)(qword_141ABD470 + 48));
                if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                  && (v1012 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v1012) >> 3 > v1011)
                  && (v1013 = *(_QWORD *)(v1012 + 8 * v1011)) != 0 )
                {
                  MEMORY[0x1419475D8](a1: v1013 + 32, a2: v1010 - *(unsigned int *)(v1013 + 120));
                  v1014 = *(_BYTE *)(v1013 + 72) != 0
                       && _InterlockedDecrement((volatile signed __int32 *)(v1013 + 64)) != 0;
                  v1009 = v1603;
                  if ( !v1014 && *(_BYTE *)(v1013 + 97) != 0 )
                    sub_1412D33C0(a1: v1013);
                }
                else
                {
                  MEMORY[0x141948990](a1: v1010 - *(unsigned int *)(qword_141ABD470 + 48));
                }
              }
              v1009[12] = v990;
              v1009[13] = v990 + 8 * (v996 + 1);
              v1009[14] = v990 + 8 * v1008;
            }
          }
        }
        *(_QWORD *)(v990 + 8 * v996) = v987;
        a1 = v1603;
        goto LABEL_1913;
      }
      v1015 = (__int64 *)(v990 + 8 * v996);
      v1016 = v1603;
      if ( v991 == (__int64 *)v1603[14] )
      {
        v1029 = v992 >> 3;
        v1030 = v1029 + (v1029 >> 1);
        v1584 = v1029 + 1;
        if ( v1030 <= v1029 + 1 )
          v1030 = v1029 + 1;
        if ( v1029 > 0x1FFFFFFFFFFFFFFFLL - (v1029 >> 1) )
          v1030 = 0x1FFFFFFFFFFFFFFFLL;
        v1031 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v1030);
        *(_QWORD *)(v1031 + 8 * v996) = v987;
        v1032 = (__int64 *)v1016[13];
        sub_141758A00(a1: v1031, a2: v1016[12], a3: (char *)v1015 - v1016[12]);
        if ( v1032 != v1015 )
          sub_141758A00(a1: v1031 + 8 * v996 + 8, a2: v1015, a3: v1016[13] - (_QWORD)v1015);
        v1033 = v1016[12];
        a1 = v1016;
        if ( v1033 != 0 )
        {
          v1034 = v1016[14] - v1033;
          if ( v1034 == -1 )
            v1034 = *(unsigned int *)(v1033 - *(unsigned int *)(qword_141ABD470 + 48));
          if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
            && (v1035 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v1035) >> 3 > v1034)
            && (v1036 = *(_QWORD *)(v1035 + 8 * v1034)) != 0 )
          {
            MEMORY[0x1419475D8](a1: v1036 + 32, a2: v1033 - *(unsigned int *)(v1036 + 120));
            v1037 = *(_BYTE *)(v1036 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1036 + 64)) != 0;
            if ( !v1037 && *(_BYTE *)(v1036 + 97) != 0 )
              sub_1412D33C0(a1: v1036);
          }
          else
          {
            MEMORY[0x141948990](a1: v1033 - *(unsigned int *)(qword_141ABD470 + 48));
          }
        }
        v1016[12] = v1031;
        v1016[13] = v1031 + 8 * v1584;
        v1016[14] = v1031 + 8 * v1030;
        goto LABEL_1913;
      }
      if ( v991 == v1015 )
      {
        *v991 = v987;
        a1 = v1603;
LABEL_1998:
        a1[13] += 8LL;
        goto LABEL_1913;
      }
      *v991 = *(v991 - 1);
      v1017 = v1603;
      v1603[13] += 8LL;
      sub_141758A00(a1: v1015 + 1, a2: v1015, a3: (char *)(v991 - 1) - (char *)v1015);
      *v1015 = v987;
      a1 = v1017;
LABEL_1913:
      LODWORD(v10) = (unsigned __int8)v1604;
LABEL_1914:
      v957 = v1598 + 1;
      if ( (int)v1598 + 1 >= (int)v1600 )
        goto LABEL_443;
    }
    a1 = v1603;
    if ( v991 == (__int64 *)v1603[14] )
    {
      v1018 = (unsigned __int64)(v992 >> 3) >> 1;
      v1019 = 0x1FFFFFFFFFFFFFFFLL - v1018;
      v1020 = (v992 >> 3) + v1018;
      v1584 = (v992 >> 3) + 1;
      if ( v1020 <= v1584 )
        v1020 = (v992 >> 3) + 1;
      if ( v992 >> 3 > v1019 )
        v1020 = 0x1FFFFFFFFFFFFFFFLL;
      v1556 = v1020;
      v1021 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v1020);
      *(_QWORD *)(v1021 + v992) = v987;
      v1022 = (__int64 *)a1[13];
      sub_141758A00(a1: v1021, a2: a1[12], a3: (char *)v991 - a1[12]);
      if ( v1022 != v991 )
        sub_141758A00(a1: v1021 + v992 + 8, a2: v991, a3: a1[13] - (_QWORD)v991);
      v1023 = v1021;
      v1024 = a1[12];
      LODWORD(v10) = (unsigned __int8)v1604;
      if ( v1024 != 0 )
      {
        v1025 = a1[14] - v1024;
        if ( v1025 == -1 )
          v1025 = *(unsigned int *)(v1024 - *(unsigned int *)(qword_141ABD470 + 48));
        if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
          && (v1026 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v1026) >> 3 > v1025)
          && (v1027 = *(_QWORD *)(v1026 + 8 * v1025)) != 0 )
        {
          MEMORY[0x1419475D8](a1: v1027 + 32, a2: v1024 - *(unsigned int *)(v1027 + 120));
          v1028 = *(_BYTE *)(v1027 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1027 + 64)) != 0;
          if ( !v1028 && *(_BYTE *)(v1027 + 97) != 0 )
            sub_1412D33C0(a1: v1027);
        }
        else
        {
          MEMORY[0x141948990](a1: v1024 - *(unsigned int *)(qword_141ABD470 + 48));
        }
      }
      a1[12] = v1023;
      a1[13] = v1023 + 8 * v1584;
      a1[14] = v1023 + 8 * v1556;
      goto LABEL_1914;
    }
    *v991 = v987;
    goto LABEL_1998;
  }
  LOBYTE(v32) = 1;
  if ( (int)v1600 > 0 )
  {
    v332 = 0;
    while ( 1 )
    {
      v1588 = 0;
      memset(v1587, 0, sizeof(v1587));
      LODWORD(v1589) = 0;
      WORD2(v1589) = -1;
      BYTE6(v1589) = -1;
      v1579 = v1596;
      if ( v1596 != nullptr )
        _InterlockedIncrement(v1596 + 2);
      v333 = sub_140ED71C0(a1: v1587, a2: &v1579, a3: (unsigned int)v1599);
      v334 = v1579;
      if ( v1579 != nullptr && _InterlockedDecrement(v1579 + 2) == 0 )
        (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v334)(a1: v334, a2: 1);
      if ( v333 == 0 )
        break;
      sub_140ED6F10(a1: v1587);
      sub_140E44A40(a1: (char *)&v1588 + 8);
      v335 = v1588;
      if ( (_QWORD)v1588 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1588 - 4)) == 0 )
        sub_1412EC9A0(a1: v335 - 4);
      v336 = v1587[3];
      if ( v1587[3] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[3] - 4LL)) == 0 )
        sub_1412EC9A0(a1: v336 - 4);
      v337 = v1587[2];
      if ( v1587[2] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[2] - 4LL)) == 0 )
        sub_1412EC9A0(a1: v337 - 4);
      v338 = v1587[1];
      if ( v1587[1] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[1] - 4LL)) == 0 )
        sub_1412EC9A0(a1: v338 - 4);
      v339 = v1587[0];
      if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] - 4LL)) == 0 )
        sub_1412EC9A0(a1: v339 - 4);
      if ( ++v332 >= (int)v1600 )
      {
        a1 = v1603;
        goto LABEL_443;
      }
    }
    sub_140E44A40(a1: (char *)&v1588 + 8);
    v1063 = v1588;
    if ( (_QWORD)v1588 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1588 - 4)) == 0 )
      sub_1412EC9A0(a1: v1063 - 4);
    v1064 = v1587[3];
    a1 = v1603;
    if ( v1587[3] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[3] - 4LL)) == 0 )
      sub_1412EC9A0(a1: v1064 - 4);
    v1065 = v1587[2];
    if ( v1587[2] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[2] - 4LL)) == 0 )
      sub_1412EC9A0(a1: v1065 - 4);
    v1066 = v1587[1];
    if ( v1587[1] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[1] - 4LL)) == 0 )
      sub_1412EC9A0(a1: v1066 - 4);
    v1067 = v1587[0];
    if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] - 4LL)) == 0 )
      sub_1412EC9A0(a1: v1067 - 4);
    goto LABEL_442;
  }
LABEL_443:
  v281 = v1596;
  if ( v1596 != nullptr && _InterlockedDecrement(v1596 + 2) == 0 )
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v281)(a1: v281, a2: 1);
  if ( (_BYTE)v32 != 0 )
  {
LABEL_447:
    if ( (_BYTE)v1597 != 0 )
      return (unsigned int)v32;
    sub_14121A480(a1: &v1579);
    if ( ((unsigned __int8)v10 & v1564) == 0 )
      goto LABEL_950;
    v282 = *((_DWORD *)a1 + 92);
    v32 = (__int64)&v1583;
    sub_14080D0E0(a1: &v1583, a2: 0x1418E2C24LL);
    LODWORD(v1597) = v282;
    v1594 = v282;
    v1586 = 23;
    sub_1408085A0(a1: &v1600, a2: &v1586);
    sub_1408085A0(a1: &v1596, a2: &v1594);
    v1602 = nullptr;
    v283 = (int *)v1596;
    if ( v1596 != nullptr )
    {
      _InterlockedIncrement(v1596 - 1);
      v1602 = v283;
      v284 = *v283;
    }
    else
    {
      v284 = 0;
    }
    v513 = v284 + 1;
    v514 = sub_1412EC810(a1: 264, a2: (unsigned int)(v284 + 1));
    v515 = (volatile signed __int32 *)v514;
    *(_DWORD *)v514 = 0;
    v516 = 0;
    if ( v284 + 1 <= 0 )
      v513 = 0;
    *(_DWORD *)(v514 + 4) = v513;
    v517 = v514 + 8;
    *(_BYTE *)(v514 + 8) = 0;
    if ( v284 <= 0 )
    {
      v519 = (_BYTE *)(v514 + 8);
      if ( v284 == 0 )
        goto LABEL_922;
    }
    else
    {
      v518 = 0x1419435F1LL;
      if ( v1602 != nullptr )
        v518 = (__int64)(v1602 + 1);
      sub_141758A00(a1: v514 + 8, a2: v518, a3: (unsigned int)v284);
      v519 = (_BYTE *)(v517 + (unsigned int)v284);
LABEL_922:
      *v519 = 0;
      v516 = v284;
    }
    v520 = v514 + 4;
    *(_WORD *)(v517 + v516) = 95;
    v521 = v1602 - 1;
    if ( v1602 != nullptr && _InterlockedDecrement(v521) == 0 )
      sub_1412EC9A0(a1: v521);
    v1602 = nullptr;
    _InterlockedIncrement(v515);
    v1602 = (volatile signed __int32 *)v520;
    sub_140809550(a1: &v1602, a2: v1587, a3: &v1600);
    v1593 = 0;
    v522 = v1587[0];
    if ( v1587[0] != 0 )
    {
      _InterlockedIncrement((volatile signed __int32 *)(v1587[0] - 4LL));
      v523 = v1587[0];
      v1593 = v522;
      if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] - 4LL)) == 0 )
        sub_1412EC9A0(a1: v523 - 4);
    }
    v524 = v1602;
    a1 = v1603;
    if ( v1602 != nullptr && _InterlockedDecrement(v1602 - 1) == 0 )
      sub_1412EC9A0(a1: v524 - 1);
    v525 = v1596;
    if ( v1596 != nullptr && _InterlockedDecrement(v1596 - 1) == 0 )
      sub_1412EC9A0(a1: v525 - 1);
    v526 = v1600;
    if ( v1600 != nullptr && _InterlockedDecrement(v1600 - 1) == 0 )
      sub_1412EC9A0(a1: v526 - 1);
    v1587[0] = 0x80100004E554C4CLL;
    LOBYTE(v1553) = 0;
    sub_1407D0F70(
      a1: (unsigned int)v1587,
      a2: (unsigned int)&v1595,
      a3: a2,
      a4: (unsigned int)&v1593,
      a5: (__int64)&v1583,
      a6: 0,
      a7: 0,
      v1553);
    v527 = v1593;
    if ( v1593 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1593 - 4)) == 0 )
      sub_1412EC9A0(a1: v527 - 4);
    v528 = v1595;
    if ( v1595 == nullptr )
      goto LABEL_2928;
    v529 = a1[34] != a1[33];
    LODWORD(v1602) = 0;
    (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **, __int64))(*(_QWORD *)v1595 + 40LL))(
      a1: v1595,
      a2: &v1602,
      a3: 4);
    if ( *((_DWORD *)v528 + 4) != 0 )
    {
LABEL_945:
      LODWORD(v1599) = 0;
      goto LABEL_946;
    }
    LODWORD(v740) = (_DWORD)v1602;
    if ( v1601 != 0 )
    {
      LOBYTE(v530) = 1;
      LODWORD(v1599) = v530;
      if ( (int)v1602 <= 0 )
        goto LABEL_946;
      v741 = 0;
      v32 = (__int64)&v1587[3];
      v742 = v1597;
      do
      {
        memset(v1587, 0, sizeof(v1587));
        WORD2(v1588) = -1;
        BYTE6(v1588) = -1;
        LODWORD(v1588) = 0;
        v1600 = v1595;
        if ( v1595 != nullptr )
          _InterlockedIncrement(v1595 + 2);
        v743 = sub_14158B750(a1: v1587, a2: &v1600, a3: v742);
        v744 = v1600;
        if ( v1600 != nullptr && _InterlockedDecrement(v1600 + 2) == 0 )
          (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v744)(a1: v744, a2: 1);
        if ( v743 == 0 )
        {
          sub_140E44A40(a1: &v1587[3]);
          v1338 = v1587[2];
          if ( v1587[2] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[2] - 4LL)) == 0 )
            sub_1412EC9A0(a1: v1338 - 4);
          v1339 = v1587[1];
          a1 = v1603;
          if ( v1587[1] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[1] - 4LL)) == 0 )
            sub_1412EC9A0(a1: v1339 - 4);
          v1340 = v1587[0];
          if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] - 4LL)) == 0 )
            sub_1412EC9A0(a1: v1340 - 4);
          goto LABEL_945;
        }
        sub_14158B5D0(a1: v1587);
        sub_140E44A40(a1: &v1587[3]);
        v745 = v1587[2];
        if ( v1587[2] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[2] - 4LL)) == 0 )
          sub_1412EC9A0(a1: v745 - 4);
        v746 = v1587[1];
        if ( v1587[1] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[1] - 4LL)) == 0 )
          sub_1412EC9A0(a1: v746 - 4);
        v747 = v1587[0];
        if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] - 4LL)) == 0 )
          sub_1412EC9A0(a1: v747 - 4);
        ++v741;
      }
      while ( v741 < (int)v1602 );
      a1 = v1603;
LABEL_946:
      v531 = v1595;
      if ( v1595 != nullptr && _InterlockedDecrement(v1595 + 2) == 0 )
        (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v531)(a1: v531, a2: 1);
      if ( (_BYTE)v1599 == 0 )
        goto LABEL_2928;
LABEL_950:
      if ( (v1605 & (unsigned __int8)(v10 & v1566)) == 0 )
        goto LABEL_2874;
      v532 = *((_DWORD *)a1 + 92);
      v32 = (__int64)&v1583;
      sub_14080D0E0(a1: &v1583, a2: 0x1418E2C24LL);
      v1594 = v532;
      v1586 = 19;
      sub_1408085A0(a1: &v1600, a2: &v1586);
      sub_1408085A0(a1: &v1596, a2: &v1594);
      v1602 = nullptr;
      v533 = (int *)v1596;
      if ( v1596 != nullptr )
      {
        _InterlockedIncrement(v1596 - 1);
        v1602 = v533;
        v534 = *v533;
      }
      else
      {
        v534 = 0;
      }
      v721 = v534 + 1;
      v722 = sub_1412EC810(a1: 264, a2: (unsigned int)(v534 + 1));
      v723 = (volatile signed __int32 *)v722;
      *(_DWORD *)v722 = 0;
      v724 = 0;
      if ( v534 + 1 <= 0 )
        v721 = 0;
      *(_DWORD *)(v722 + 4) = v721;
      v725 = v722 + 8;
      *(_BYTE *)(v722 + 8) = 0;
      if ( v534 <= 0 )
      {
        v727 = (_BYTE *)(v722 + 8);
        if ( v534 == 0 )
          goto LABEL_1358;
      }
      else
      {
        v726 = 0x1419435F1LL;
        if ( v1602 != nullptr )
          v726 = (__int64)(v1602 + 1);
        sub_141758A00(a1: v722 + 8, a2: v726, a3: (unsigned int)v534);
        v727 = (_BYTE *)(v725 + (unsigned int)v534);
LABEL_1358:
        *v727 = 0;
        v724 = v534;
      }
      v728 = v722 + 4;
      *(_WORD *)(v725 + v724) = 95;
      v729 = v1602 - 1;
      if ( v1602 != nullptr && _InterlockedDecrement(v729) == 0 )
        sub_1412EC9A0(a1: v729);
      v1602 = nullptr;
      _InterlockedIncrement(v723);
      v1602 = (volatile signed __int32 *)v728;
      sub_140809550(a1: &v1602, a2: v1587, a3: &v1600);
      v1593 = 0;
      v730 = v1587[0];
      if ( v1587[0] != 0 )
      {
        _InterlockedIncrement((volatile signed __int32 *)(v1587[0] - 4LL));
        v731 = v1587[0];
        v1593 = v730;
        if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] - 4LL)) == 0 )
          sub_1412EC9A0(a1: v731 - 4);
      }
      v732 = v1602;
      v733 = v1603;
      if ( v1602 != nullptr && _InterlockedDecrement(v1602 - 1) == 0 )
        sub_1412EC9A0(a1: v732 - 1);
      v734 = v1596;
      if ( v1596 != nullptr && _InterlockedDecrement(v1596 - 1) == 0 )
        sub_1412EC9A0(a1: v734 - 1);
      v735 = v1600;
      if ( v1600 != nullptr && _InterlockedDecrement(v1600 - 1) == 0 )
        sub_1412EC9A0(a1: v735 - 1);
      v1587[0] = 0x80100004E554C4CLL;
      LOBYTE(v1553) = 0;
      sub_1407D0F70(
        a1: (unsigned int)v1587,
        a2: (unsigned int)&v1595,
        a3: a2,
        a4: (unsigned int)&v1593,
        a5: (__int64)&v1583,
        a6: 0,
        a7: 0,
        v1553);
      v736 = v1593;
      if ( v1593 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1593 - 4)) == 0 )
        sub_1412EC9A0(a1: v736 - 4);
      v737 = v1595;
      if ( v1595 == nullptr )
        goto LABEL_2928;
      v738 = v733[28] != v733[27];
      LODWORD(v1596) = 0;
      (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **, __int64))(*(_QWORD *)v1595 + 40LL))(
        a1: v1595,
        a2: &v1596,
        a3: 4);
      if ( *((_DWORD *)v737 + 4) != 0 )
      {
        LOBYTE(v739) = 0;
        goto LABEL_2870;
      }
      if ( v1601 != 0 )
      {
        LOBYTE(v739) = 1;
        if ( (int)v1596 <= 0 )
          goto LABEL_2870;
        v944 = 0;
        v32 = (__int64)&v1602;
        while ( 2 )
        {
          BYTE4(v1587[0]) = -1;
          LODWORD(v1587[0]) = 0;
          *(_OWORD *)&v1587[1] = 0u;
          v1600 = v1595;
          _InterlockedIncrement(v1595 + 2);
          v945 = v1600;
          (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *, __int64))(*(_QWORD *)v1600 + 40LL))(
            a1: v1600,
            a2: v1587,
            a3: 4);
          if ( *((_DWORD *)v945 + 4) != 0 || (sub_140814B10(a1: v1600, a2: &v1602, a3: &v1587[1]), (_DWORD)v1602 != 0) )
            v946 = 0;
          else
            v946 = sub_140E45290(a1: &v1587[2], a2: &v1600);
          v947 = v1600;
          if ( v1600 != nullptr && _InterlockedDecrement(v1600 + 2) == 0 )
            (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v947)(a1: v947, a2: 1);
          if ( v946 != 0 )
          {
            sub_14157CD50(a1: v1587);
            sub_140E44A40(a1: &v1587[2]);
            v948 = v1587[1];
            if ( v1587[1] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[1] - 4LL)) == 0 )
              sub_1412EC9A0(a1: v948 - 4);
            if ( ++v944 < (int)v1596 )
              continue;
            LODWORD(v10) = (unsigned __int8)v1604;
            LOBYTE(v739) = 1;
LABEL_2870:
            v1440 = v1595;
            if ( v1595 != nullptr && _InterlockedDecrement(v1595 + 2) == 0 )
              (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v1440)(a1: v1440, a2: 1);
            a1 = v1603;
            if ( (_BYTE)v739 == 0 )
              goto LABEL_2928;
LABEL_2874:
            if ( (v1605 & (unsigned __int8)(v10 & v1567)) == 0 )
              goto LABEL_2912;
            v1441 = *((_DWORD *)a1 + 92);
            sub_14080D0E0(a1: &v1583, a2: 0x1418E2C24LL);
            LODWORD(v1599) = v1441;
            v1594 = v1441;
            v1586 = 56;
            sub_1408085A0(a1: &v1600, a2: &v1586);
            sub_1408085A0(a1: &v1596, a2: &v1594);
            v1602 = nullptr;
            v1442 = (int *)v1596;
            LODWORD(v32) = v10;
            if ( v1596 != nullptr )
            {
              _InterlockedIncrement(v1596 - 1);
              v1602 = v1442;
              v1443 = *v1442;
            }
            else
            {
              v1443 = 0;
            }
            v1444 = a1;
            v1445 = v1443 + 1;
            v1446 = sub_1412EC810(a1: 264, a2: (unsigned int)(v1443 + 1));
            v1447 = (volatile signed __int32 *)v1446;
            *(_DWORD *)v1446 = 0;
            v1448 = 0;
            if ( v1443 + 1 <= 0 )
              v1445 = 0;
            *(_DWORD *)(v1446 + 4) = v1445;
            v1449 = v1446 + 8;
            *(_BYTE *)(v1446 + 8) = 0;
            if ( v1443 <= 0 )
            {
              v1451 = (_BYTE *)(v1446 + 8);
              if ( v1443 == 0 )
                goto LABEL_2884;
            }
            else
            {
              v1450 = 0x1419435F1LL;
              if ( v1602 != nullptr )
                v1450 = (__int64)(v1602 + 1);
              sub_141758A00(a1: v1446 + 8, a2: v1450, a3: (unsigned int)v1443);
              v1451 = (_BYTE *)(v1449 + (unsigned int)v1443);
LABEL_2884:
              *v1451 = 0;
              v1448 = v1443;
            }
            v1452 = v1446 + 4;
            *(_WORD *)(v1449 + v1448) = 95;
            v1453 = v1602 - 1;
            if ( v1602 != nullptr && _InterlockedDecrement(v1453) == 0 )
              sub_1412EC9A0(a1: v1453);
            v1602 = nullptr;
            _InterlockedIncrement(v1447);
            v1602 = (volatile signed __int32 *)v1452;
            sub_140809550(a1: &v1602, a2: v1587, a3: &v1600);
            v1593 = 0;
            v1454 = v1587[0];
            if ( v1587[0] != 0 )
            {
              _InterlockedIncrement((volatile signed __int32 *)(v1587[0] - 4LL));
              v1455 = v1587[0];
              v1593 = v1454;
              if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] - 4LL)) == 0 )
                sub_1412EC9A0(a1: v1455 - 4);
            }
            v1456 = v1602;
            a1 = v1444;
            if ( v1602 != nullptr && _InterlockedDecrement(v1602 - 1) == 0 )
              sub_1412EC9A0(a1: v1456 - 1);
            v1457 = v1596;
            LOBYTE(v10) = v32;
            if ( v1596 != nullptr && _InterlockedDecrement(v1596 - 1) == 0 )
              sub_1412EC9A0(a1: v1457 - 1);
            v1458 = v1600;
            if ( v1600 != nullptr && _InterlockedDecrement(v1600 - 1) == 0 )
              sub_1412EC9A0(a1: v1458 - 1);
            v1587[0] = 0x80100004E554C4CLL;
            LOBYTE(v1553) = 0;
            sub_1407D0F70(
              a1: (unsigned int)v1587,
              a2: (unsigned int)&v1595,
              a3: a2,
              a4: (unsigned int)&v1593,
              a5: (__int64)&v1583,
              a6: 0,
              a7: 0,
              v1553);
            v1459 = v1593;
            if ( v1593 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1593 - 4)) == 0 )
              sub_1412EC9A0(a1: v1459 - 4);
            v1460 = v1595;
            if ( v1595 == nullptr )
              goto LABEL_2928;
            v1461 = a1[43] != a1[42];
            LODWORD(v1602) = 0;
            (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **, __int64))(*(_QWORD *)v1595 + 40LL))(
              a1: v1595,
              a2: &v1602,
              a3: 4);
            if ( *((_DWORD *)v1460 + 4) != 0 )
            {
LABEL_2907:
              LOBYTE(v1462) = 0;
              goto LABEL_2908;
            }
            if ( v1601 != 0 )
            {
              LOBYTE(v1462) = 1;
              if ( (int)v1602 <= 0 )
                goto LABEL_2908;
              v1474 = 0;
              v32 = (__int64)&v1600;
              v1475 = v1599;
              while ( 1 )
              {
                memset(v1587, 0, 28);
                WORD2(v1587[3]) = -1;
                v1600 = v1595;
                if ( v1595 != nullptr )
                  _InterlockedIncrement(v1595 + 2);
                v1476 = sub_14159D1F0(a1: v1587, a2: &v1600, a3: v1475);
                v1477 = v1600;
                if ( v1600 != nullptr && _InterlockedDecrement(v1600 + 2) == 0 )
                  (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v1477)(a1: v1477, a2: 1);
                if ( v1476 == 0 )
                  break;
                sub_14159D0E0(a1: v1587);
                v1478 = v1587[2];
                if ( v1587[2] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[2] - 4LL)) == 0 )
                  sub_1412EC9A0(a1: v1478 - 4);
                v1479 = v1587[1];
                if ( v1587[1] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[1] - 4LL)) == 0 )
                  sub_1412EC9A0(a1: v1479 - 4);
                sub_140E44A40(a1: v1587);
                if ( ++v1474 >= (int)v1602 )
                  goto LABEL_2970;
              }
              v1536 = v1587[2];
              if ( v1587[2] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[2] - 4LL)) == 0 )
                sub_1412EC9A0(a1: v1536 - 4);
              v1537 = v1587[1];
              if ( v1587[1] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[1] - 4LL)) == 0 )
                sub_1412EC9A0(a1: v1537 - 4);
              sub_140E44A40(a1: v1587);
              goto LABEL_2907;
            }
            v1480 = (int)v1602;
            v1481 = v1461;
            if ( v1461 )
            {
              v1482 = a1[42];
              v1483 = (a1[43] - v1482) >> 3;
              v1484 = v1483 + (int)v1602;
              v1485 = (a1[44] - v1482) >> 3;
              if ( v1485 >= v1484 )
                goto LABEL_2967;
              if ( v1484 >> 61 == 0 )
              {
                v32 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v1484);
                sub_141758A00(a1: v32, a2: a1[42], a3: a1[43] - a1[42]);
                if ( a1[42] != 0 )
                  sub_1407E4890(a1: qword_141ABD470);
                a1[42] = v32;
                a1[43] = v32 + 8 * v1483;
                a1[44] = v32 + 8 * v1484;
                goto LABEL_2967;
              }
LABEL_3126:
              sub_1400526C0(a1: v1485);
            }
            v32 = a1[42];
            v1485 = (a1[44] - v32) >> 3;
            if ( v1485 < (int)v1602 )
            {
              if ( (int)v1602 < 0 )
                goto LABEL_3126;
              v1486 = a1[43];
              v1487 = a1;
              v1488 = sub_1407E4490(a1: qword_141ABD470, a2: 8LL * (int)v1602);
              sub_141758A00(a1: v1488, a2: v1487[42], a3: v1487[43] - v1487[42]);
              if ( v1487[42] != 0 )
                sub_1407E4890(a1: qword_141ABD470);
              v1487[42] = v1488;
              v1487[43] = v1488 + v1486 - v32;
              v1487[44] = v1488 + 8 * v1480;
              a1 = v1487;
            }
LABEL_2967:
            if ( (int)v1602 <= 0 )
            {
LABEL_2970:
              LOBYTE(v1462) = 1;
              goto LABEL_2908;
            }
            if ( !v1481 )
            {
              v1538 = 0;
              LODWORD(v32) = v1599;
              do
              {
                if ( dword_141B607B8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer
                                                   + (unsigned int)TlsIndex)
                                                 + 4LL) )
                {
                  sub_141750E08(a1: &dword_141B607B8);
                  if ( dword_141B607B8 == -1 )
                  {
                    sub_1407E53D0(
                      a1: (unsigned int)&unk_141B60768,
                      a2: 1100150614,
                      a3: 64,
                      a4: 32,
                      a5: 0,
                      a6: 1,
                      a7: 64,
                      a8: 4096);
                    sub_141751048(a1: sub_140FE1110);
                    sub_141750EA0(a1: &dword_141B607B8);
                  }
                }
                v1539 = sub_1407E58C0(a1: &unk_141B60768, a2: 32);
                *(_QWORD *)v1539 = 0;
                *(_QWORD *)(v1539 + 8) = 0;
                *(_QWORD *)(v1539 + 16) = 0;
                *(_WORD *)(v1539 + 28) = -1;
                *(_DWORD *)(v1539 + 24) = 0;
                v1587[0] = v1595;
                if ( v1595 != nullptr )
                  _InterlockedIncrement(v1595 + 2);
                LODWORD(v1462) = sub_14159D1F0(a1: v1539, a2: v1587, a3: (unsigned int)v32);
                v1540 = (void (__fastcall ***)(_QWORD, __int64))v1587[0];
                if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] + 8LL)) == 0 )
                  (**v1540)(a1: v1540, a2: 1);
                if ( (_BYTE)v1462 == 0 )
                  break;
                v1541 = (__int64 *)a1[43];
                if ( v1541 == (__int64 *)a1[44] )
                {
                  LODWORD(v1598) = v1538;
                  LODWORD(v1597) = v1462;
                  v1542 = (__int64)v1541 - a1[42];
                  v1543 = v1542 >> 3;
                  v10 = (__int64)a1;
                  v1544 = (unsigned __int64)(v1542 >> 3) >> 1;
                  v1545 = 0x1FFFFFFFFFFFFFFFLL - v1544;
                  v1462 = (v1542 >> 3) + v1544;
                  v1584 = (v1542 >> 3) + 1;
                  if ( v1462 <= v1584 )
                    v1462 = v1543 + 1;
                  if ( v1543 > v1545 )
                    v1462 = 0x1FFFFFFFFFFFFFFFLL;
                  v1546 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v1462);
                  *(_QWORD *)(v1546 + v1542) = v1539;
                  v1547 = *(__int64 **)(v10 + 344);
                  sub_141758A00(a1: v1546, a2: *(_QWORD *)(v10 + 336), a3: (char *)v1541 - *(_QWORD *)(v10 + 336));
                  if ( v1547 != v1541 )
                    sub_141758A00(a1: v1546 + v1542 + 8, a2: v1541, a3: *(_QWORD *)(v10 + 344) - (_QWORD)v1541);
                  v1548 = *(_QWORD *)(v10 + 336);
                  if ( v1548 != 0 )
                  {
                    v1549 = *(_QWORD *)(v10 + 352) - v1548;
                    if ( v1549 == -1 )
                      v1549 = *(unsigned int *)(v1548 - *(unsigned int *)(qword_141ABD470 + 48));
                    if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                      && (v1550 = *(_QWORD *)(qword_141ABD470 + 24),
                          (*(_QWORD *)(qword_141ABD470 + 32) - v1550) >> 3 > v1549)
                      && (v1551 = *(_QWORD *)(v1550 + 8 * v1549)) != 0 )
                    {
                      MEMORY[0x1419475D8](a1: v1551 + 32, a2: v1548 - *(unsigned int *)(v1551 + 120));
                      v1552 = *(_BYTE *)(v1551 + 72) != 0
                           && _InterlockedDecrement((volatile signed __int32 *)(v1551 + 64)) != 0;
                      v10 = (__int64)v1603;
                      if ( !v1552 && *(_BYTE *)(v1551 + 97) != 0 )
                        sub_1412D33C0(a1: v1551);
                    }
                    else
                    {
                      MEMORY[0x141948990](a1: v1548 - *(unsigned int *)(qword_141ABD470 + 48));
                      v10 = (__int64)v1603;
                    }
                  }
                  *(_QWORD *)(v10 + 336) = v1546;
                  *(_QWORD *)(v10 + 344) = v1546 + 8 * v1584;
                  *(_QWORD *)(v10 + 352) = v1546 + 8 * v1462;
                  a1 = (_QWORD *)v10;
                  LOBYTE(v10) = v1604;
                  LODWORD(v32) = v1599;
                  LOBYTE(v1462) = v1597;
                  v1538 = v1598;
                }
                else
                {
                  *v1541 = v1539;
                  a1[43] += 8LL;
                }
                ++v1538;
              }
              while ( v1538 < (int)v1602 );
              goto LABEL_2908;
            }
            v1489 = 0;
            v1490 = v1599;
            while ( 2 )
            {
              LODWORD(v1598) = v1489;
              if ( dword_141B607B8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer
                                                 + (unsigned int)TlsIndex)
                                               + 4LL) )
              {
                sub_141750E08(a1: &dword_141B607B8);
                if ( dword_141B607B8 == -1 )
                {
                  sub_1407E53D0(
                    a1: (unsigned int)&unk_141B60768,
                    a2: 1100150614,
                    a3: 64,
                    a4: 32,
                    a5: 0,
                    a6: 1,
                    a7: 64,
                    a8: 4096);
                  sub_141751048(a1: sub_140FE1110);
                  sub_141750EA0(a1: &dword_141B607B8);
                }
              }
              v32 = sub_1407E58C0(a1: &unk_141B60768, a2: 32);
              *(_QWORD *)v32 = 0;
              *(_QWORD *)(v32 + 8) = 0;
              *(_QWORD *)(v32 + 16) = 0;
              *(_WORD *)(v32 + 28) = -1;
              *(_DWORD *)(v32 + 24) = 0;
              v1587[0] = v1595;
              if ( v1595 != nullptr )
                _InterlockedIncrement(v1595 + 2);
              v1491 = sub_14159D1F0(a1: v32, a2: v1587, a3: v1490);
              v1492 = (void (__fastcall ***)(_QWORD, __int64))v1587[0];
              if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] + 8LL)) == 0 )
                (**v1492)(a1: v1492, a2: 1);
              if ( (_BYTE)v1491 != 0 )
              {
                LODWORD(v1597) = v1491;
                v1493 = a1[42];
                v1494 = (__int64 *)a1[43];
                v1495 = (__int64)v1494 - v1493;
                v1496 = (__int64 *)v1493;
                if ( (__int64)v1494 - v1493 > 0 )
                {
                  v1497 = (unsigned __int64)v1495 >> 3;
                  v1496 = (__int64 *)a1[42];
                  v1498 = (unsigned __int64)v1495 >> 3;
                  do
                  {
                    v1498 = (unsigned __int64)v1498 >> 1;
                    if ( *(_DWORD *)(v1496[v1498] + 24) < *(_DWORD *)(v32 + 24) )
                    {
                      v1496 += v1498 + 1;
                      v1498 = v1497 + ~v1498;
                    }
                    v1497 = v1498;
                  }
                  while ( v1498 > 0 );
                }
                if ( v1496 == v1494 )
                {
                  a1 = v1603;
                  if ( v1494 == (__int64 *)v1603[44] )
                  {
                    v1516 = (unsigned __int64)(v1495 >> 3) >> 1;
                    v1517 = 0x1FFFFFFFFFFFFFFFLL - v1516;
                    v1518 = (v1495 >> 3) + v1516;
                    v1584 = (v1495 >> 3) + 1;
                    if ( v1518 <= v1584 )
                      v1518 = (v1495 >> 3) + 1;
                    v1519 = v1518;
                    if ( v1495 >> 3 > v1517 )
                      v1519 = 0x1FFFFFFFFFFFFFFFLL;
                    v10 = (__int64)v1603;
                    v1520 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v1519);
                    *(_QWORD *)(v1520 + v1495) = v32;
                    v1521 = *(__int64 **)(v10 + 344);
                    sub_141758A00(a1: v1520, a2: *(_QWORD *)(v10 + 336), a3: (char *)v1494 - *(_QWORD *)(v10 + 336));
                    if ( v1521 != v1494 )
                      sub_141758A00(a1: v1520 + v1495 + 8, a2: v1494, a3: *(_QWORD *)(v10 + 344) - (_QWORD)v1494);
                    v1522 = *(_QWORD *)(v10 + 336);
                    v1490 = v1599;
                    LOBYTE(v1462) = v1597;
                    if ( v1522 != 0 )
                    {
                      v1523 = *(_QWORD *)(v10 + 352) - v1522;
                      if ( v1523 == -1 )
                        v1523 = *(unsigned int *)(v1522 - *(unsigned int *)(qword_141ABD470 + 48));
                      if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                        && (v1524 = *(_QWORD *)(qword_141ABD470 + 24),
                            (*(_QWORD *)(qword_141ABD470 + 32) - v1524) >> 3 > v1523)
                        && (v32 = *(_QWORD *)(v1524 + 8 * v1523)) != 0 )
                      {
                        MEMORY[0x1419475D8](a1: v32 + 32, a2: v1522 - *(unsigned int *)(v32 + 120));
                        v1525 = *(_BYTE *)(v32 + 72) != 0
                             && _InterlockedDecrement((volatile signed __int32 *)(v32 + 64)) != 0;
                        v10 = (__int64)v1603;
                        v1490 = v1599;
                        LOBYTE(v1462) = v1597;
                        if ( !v1525 && *(_BYTE *)(v32 + 97) != 0 )
                          sub_1412D33C0(a1: v32);
                      }
                      else
                      {
                        MEMORY[0x141948990](a1: v1522 - *(unsigned int *)(qword_141ABD470 + 48));
                        v10 = (__int64)v1603;
                      }
                    }
                    *(_QWORD *)(v10 + 336) = v1520;
                    *(_QWORD *)(v10 + 344) = v1520 + 8 * v1584;
                    *(_QWORD *)(v10 + 352) = v1520 + 8 * v1519;
                    a1 = (_QWORD *)v10;
                    LOBYTE(v10) = v1604;
                    goto LABEL_2975;
                  }
                  *v1494 = v32;
                }
                else
                {
                  v1499 = ((__int64)v1496 - v1493) >> 3;
                  if ( *(_DWORD *)(*v1496 + 24) == *(_DWORD *)(v32 + 24) )
                  {
                    v1500 = v1495 >> 3;
                    if ( v1500 > v1499 )
                    {
                      v1501 = *(_QWORD *)(v1493 + 8 * v1499);
                      if ( v1501 != 0 )
                      {
                        v1502 = *(_QWORD *)(v1501 + 16);
                        if ( v1502 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1502 - 4)) == 0 )
                          sub_1412EC9A0(a1: v1502 - 4);
                        v1503 = *(_QWORD *)(v1501 + 8);
                        v1504 = v1603;
                        if ( v1503 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1503 - 4)) == 0 )
                          sub_1412EC9A0(a1: v1503 - 4);
                        sub_140E44A40(a1: v1501);
                        sub_140FE0FB0(a1: v1501);
                        v1493 = v1504[42];
                        v1494 = (__int64 *)v1504[43];
                        v1500 = ((__int64)v1494 - v1493) >> 3;
                      }
                    }
                    if ( v1500 <= v1499 )
                    {
                      v1505 = v1499 + 1;
                      v1506 = v1499 + 1 - v1500;
                      if ( v1499 + 1 < v1500 )
                      {
                        v1603[43] = v1493 + 8 * v1505;
                      }
                      else if ( v1499 + 1 > v1500 )
                      {
                        v1507 = (v1603[44] - v1493) >> 3;
                        if ( v1507 >= v1505 )
                        {
                          sub_141758A10(a1: v1494, a2: 0, a3: 8 * v1506);
                          v1534 = v1603;
                          v1603[43] = &v1494[v1506];
                          v1493 = v1534[42];
                        }
                        else
                        {
                          v1485 = v1505 >> 61;
                          if ( v1505 >> 61 != 0 )
                            goto LABEL_3126;
                          v1508 = v1507 + (v1507 >> 1);
                          if ( v1508 <= v1505 )
                            v1508 = v1499 + 1;
                          if ( v1507 > 0x1FFFFFFFFFFFFFFFLL - (v1507 >> 1) )
                            v1508 = 0x1FFFFFFFFFFFFFFFLL;
                          v1493 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v1508);
                          sub_141758A10(a1: v1493 + 8 * v1500, a2: 0, a3: 8 * v1506);
                          v1509 = v1603;
                          sub_141758A00(a1: v1493, a2: v1603[42], a3: v1603[43] - v1603[42]);
                          v1510 = v1509[42];
                          if ( v1510 != 0 )
                          {
                            v1511 = v1603[44] - v1510;
                            if ( v1511 == -1 )
                              v1511 = *(unsigned int *)(v1510 - *(unsigned int *)(qword_141ABD470 + 48));
                            if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                              && (v1512 = *(_QWORD *)(qword_141ABD470 + 24),
                                  (*(_QWORD *)(qword_141ABD470 + 32) - v1512) >> 3 > v1511)
                              && (v1513 = *(_QWORD *)(v1512 + 8 * v1511)) != 0 )
                            {
                              MEMORY[0x1419475D8](a1: v1513 + 32, a2: v1510 - *(unsigned int *)(v1513 + 120));
                              v1514 = *(_BYTE *)(v1513 + 72) != 0
                                   && _InterlockedDecrement((volatile signed __int32 *)(v1513 + 64)) != 0;
                              if ( !v1514 && *(_BYTE *)(v1513 + 97) != 0 )
                                sub_1412D33C0(a1: v1513);
                            }
                            else
                            {
                              MEMORY[0x141948990](a1: v1510 - *(unsigned int *)(qword_141ABD470 + 48));
                            }
                          }
                          v1535 = v1603;
                          v1603[42] = v1493;
                          v1535[43] = v1493 + 8 * v1505;
                          v1535[44] = v1493 + 8 * v1508;
                        }
                      }
                    }
                    *(_QWORD *)(v1493 + 8 * v1499) = v32;
                    a1 = v1603;
LABEL_2973:
                    LOBYTE(v10) = v1604;
LABEL_2974:
                    v1490 = v1599;
                    LOBYTE(v1462) = v1597;
LABEL_2975:
                    v1489 = v1598 + 1;
                    if ( (int)v1598 + 1 >= (int)v1602 )
                      goto LABEL_2908;
                    continue;
                  }
                  v1515 = (__int64 *)(v1493 + 8 * v1499);
                  v10 = (__int64)v1603;
                  if ( v1494 == (__int64 *)v1603[44] )
                  {
                    v1526 = v1495 >> 3;
                    v1527 = v1526 + (v1526 >> 1);
                    v1584 = v1526 + 1;
                    if ( v1527 <= v1526 + 1 )
                      v1527 = v1526 + 1;
                    if ( v1526 > 0x1FFFFFFFFFFFFFFFLL - (v1526 >> 1) )
                      v1527 = 0x1FFFFFFFFFFFFFFFLL;
                    v1528 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v1527);
                    *(_QWORD *)(v1528 + 8 * v1499) = v32;
                    v1529 = *(__int64 **)(v10 + 344);
                    sub_141758A00(a1: v1528, a2: *(_QWORD *)(v10 + 336), a3: (char *)v1515 - *(_QWORD *)(v10 + 336));
                    if ( v1529 != v1515 )
                      sub_141758A00(a1: v1528 + 8 * v1499 + 8, a2: v1515, a3: *(_QWORD *)(v10 + 344) - (_QWORD)v1515);
                    v1530 = *(_QWORD *)(v10 + 336);
                    a1 = (_QWORD *)v10;
                    LOBYTE(v10) = v1604;
                    if ( v1530 != 0 )
                    {
                      v1531 = a1[44] - v1530;
                      if ( v1531 == -1 )
                        v1531 = *(unsigned int *)(v1530 - *(unsigned int *)(qword_141ABD470 + 48));
                      if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                        && (v1532 = *(_QWORD *)(qword_141ABD470 + 24),
                            (*(_QWORD *)(qword_141ABD470 + 32) - v1532) >> 3 > v1531)
                        && (v32 = *(_QWORD *)(v1532 + 8 * v1531)) != 0 )
                      {
                        MEMORY[0x1419475D8](a1: v32 + 32, a2: v1530 - *(unsigned int *)(v32 + 120));
                        v1533 = *(_BYTE *)(v32 + 72) != 0
                             && _InterlockedDecrement((volatile signed __int32 *)(v32 + 64)) != 0;
                        a1 = v1603;
                        LOBYTE(v10) = v1604;
                        if ( !v1533 && *(_BYTE *)(v32 + 97) != 0 )
                          sub_1412D33C0(a1: v32);
                      }
                      else
                      {
                        MEMORY[0x141948990](a1: v1530 - *(unsigned int *)(qword_141ABD470 + 48));
                      }
                    }
                    a1[42] = v1528;
                    a1[43] = v1528 + 8 * v1584;
                    a1[44] = v1528 + 8 * v1527;
                    goto LABEL_2974;
                  }
                  if ( v1494 != v1515 )
                  {
                    *v1494 = *(v1494 - 1);
                    a1 = v1603;
                    v1603[43] += 8LL;
                    sub_141758A00(a1: v1515 + 1, a2: v1515, a3: (char *)(v1494 - 1) - (char *)v1515);
                    *v1515 = v32;
                    goto LABEL_2973;
                  }
                  *v1494 = v32;
                  a1 = v1603;
                }
                a1[43] += 8LL;
                goto LABEL_2973;
              }
              break;
            }
            LOBYTE(v1462) = 0;
            LOBYTE(v10) = v1604;
LABEL_2908:
            v1463 = v1595;
            if ( v1595 != nullptr && _InterlockedDecrement(v1595 + 2) == 0 )
              (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v1463)(a1: v1463, a2: 1);
            if ( (_BYTE)v1462 == 0 )
              goto LABEL_2928;
LABEL_2912:
            if ( (a9 & (unsigned __int8)(v10 & v1568)) != 0 )
            {
              if ( v1601 != 0 )
              {
                sub_1410BD2A0(a1: qword_141B5FFD8, a2: *((unsigned int *)a1 + 92), a3: a2, a4: a10);
              }
              else if ( (unsigned __int8)sub_1410BD2A0(a1: a1[45], a2: *((unsigned int *)a1 + 92), a3: a2, a4: a10) == 0 )
              {
                goto LABEL_2928;
              }
            }
            v85 = v1605;
            v1464 = v1605 & v10 & v1569;
            v1465 = qword_141B59FA0;
            if ( qword_141B59FA0 != 0 && v1581 != 0 )
            {
              v1466 = v1580;
              v1467 = (unsigned int)MEMORY[0x141947498]();
              v1468 = *(_QWORD *)(v1465 + 16);
              if ( v1468 == 0 || v1468 == (unsigned int)v1467 )
              {
                if ( v1466 == 0 )
                  v1467 = 0;
                *(_QWORD *)(v1465 + 16) = v1467;
              }
              *(_QWORD *)(v1465 + 8) = v1579;
              v85 = v1605;
            }
            if ( v1464 != 0 )
            {
              LODWORD(v32) = sub_140FDFBE0(a1: a1 + 30, a2: *((unsigned int *)a1 + 92), a3: a2, a4: v1601);
              if ( (_BYTE)v32 == 0 )
                return (unsigned int)v32;
              v85 = v1605;
              if ( a6 == 0 )
                return (unsigned int)v32;
            }
            else
            {
              LOBYTE(v32) = 1;
              if ( a6 == 0 )
                return (unsigned int)v32;
            }
LABEL_95:
            v1605 = v85;
            v89 = v85 & v10 & v1573;
            sub_14121A480(a1: &v1579);
            if ( v89 == 0 )
              goto LABEL_280;
            v90 = *((_DWORD *)a1 + 92);
            v32 = (__int64)&v1583;
            sub_14080D0E0(a1: &v1583, a2: 0x1418E2C24LL);
            LODWORD(v1597) = v90;
            v1594 = v90;
            v1586 = 0;
            sub_1408085A0(a1: &v1600, a2: &v1586);
            sub_1408085A0(a1: &v1596, a2: &v1594);
            v1602 = nullptr;
            v91 = (int *)v1596;
            if ( v1596 != nullptr )
            {
              _InterlockedIncrement(v1596 - 1);
              v1602 = v91;
              v92 = *v91;
            }
            else
            {
              v92 = 0;
            }
            v10 = (__int64)a1;
            v162 = v92 + 1;
            v163 = sub_1412EC810(a1: 264, a2: (unsigned int)(v92 + 1));
            v164 = (volatile signed __int32 *)v163;
            *(_DWORD *)v163 = 0;
            v165 = 0;
            if ( v92 + 1 <= 0 )
              v162 = 0;
            *(_DWORD *)(v163 + 4) = v162;
            v166 = v163 + 8;
            *(_BYTE *)(v163 + 8) = 0;
            if ( v92 <= 0 )
            {
              v168 = (_BYTE *)(v163 + 8);
              if ( v92 == 0 )
                goto LABEL_251;
            }
            else
            {
              v167 = 0x1419435F1LL;
              if ( v1602 != nullptr )
                v167 = (__int64)(v1602 + 1);
              sub_141758A00(a1: v163 + 8, a2: v167, a3: (unsigned int)v92);
              v168 = (_BYTE *)(v166 + (unsigned int)v92);
LABEL_251:
              *v168 = 0;
              v165 = v92;
            }
            v169 = v163 + 4;
            *(_WORD *)(v166 + v165) = 95;
            v170 = v1602 - 1;
            if ( v1602 != nullptr && _InterlockedDecrement(v170) == 0 )
              sub_1412EC9A0(a1: v170);
            v1602 = nullptr;
            _InterlockedIncrement(v164);
            v1602 = (volatile signed __int32 *)v169;
            sub_140809550(a1: &v1602, a2: v1587, a3: &v1600);
            v1593 = 0;
            v171 = v1587[0];
            if ( v1587[0] != 0 )
            {
              _InterlockedIncrement((volatile signed __int32 *)(v1587[0] - 4LL));
              v172 = v1587[0];
              v1593 = v171;
              if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] - 4LL)) == 0 )
                sub_1412EC9A0(a1: v172 - 4);
            }
            v173 = v1602;
            a1 = (_QWORD *)v10;
            if ( v1602 != nullptr && _InterlockedDecrement(v1602 - 1) == 0 )
              sub_1412EC9A0(a1: v173 - 1);
            v174 = v1596;
            if ( v1596 != nullptr && _InterlockedDecrement(v1596 - 1) == 0 )
              sub_1412EC9A0(a1: v174 - 1);
            v175 = v1600;
            if ( v1600 != nullptr && _InterlockedDecrement(v1600 - 1) == 0 )
              sub_1412EC9A0(a1: v175 - 1);
            v1587[0] = 0x80100004E554C4CLL;
            LOBYTE(v1553) = 0;
            sub_1407D0F70(
              a1: (unsigned int)v1587,
              a2: (unsigned int)&v1595,
              a3: a2,
              a4: (unsigned int)&v1593,
              a5: (__int64)&v1583,
              a6: 0,
              a7: 0,
              v1553);
            v176 = v1593;
            if ( v1593 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1593 - 4)) == 0 )
              sub_1412EC9A0(a1: v176 - 4);
            v177 = v1595;
            if ( v1595 == nullptr )
              goto LABEL_2928;
            v178 = *(_QWORD *)(v10 + 8) != *(_QWORD *)v10;
            LODWORD(v1602) = 0;
            (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **, __int64))(*(_QWORD *)v1595 + 40LL))(
              a1: v1595,
              a2: &v1602,
              a3: 4);
            if ( *((_DWORD *)v177 + 4) != 0 )
            {
LABEL_274:
              LODWORD(v1599) = 0;
              goto LABEL_275;
            }
            LODWORD(v245) = (_DWORD)v1602;
            if ( v1601 != 0 )
            {
              LOBYTE(v179) = 1;
              LODWORD(v1599) = v179;
              if ( (int)v1602 <= 0 )
                goto LABEL_275;
              v246 = 0;
              v32 = (__int64)&v1587[2];
              v247 = v1597;
              do
              {
                memset(v1587, 0, 28);
                WORD2(v1587[3]) = -1;
                v1600 = v1595;
                if ( v1595 != nullptr )
                  _InterlockedIncrement(v1595 + 2);
                v248 = sub_140E498B0(a1: v1587, a2: &v1600, a3: v247);
                v249 = v1600;
                if ( v1600 != nullptr && _InterlockedDecrement(v1600 + 2) == 0 )
                  (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v249)(a1: v249, a2: 1);
                if ( v248 == 0 )
                {
                  sub_140E44A40(a1: &v1587[2]);
                  v927 = v1587[1];
                  if ( v1587[1] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[1] - 4LL)) == 0 )
                    sub_1412EC9A0(a1: v927 - 4);
                  v928 = v1587[0];
                  a1 = (_QWORD *)v10;
                  if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] - 4LL)) == 0 )
                    sub_1412EC9A0(a1: v928 - 4);
                  goto LABEL_274;
                }
                sub_140E497A0(a1: v1587);
                sub_140E44A40(a1: &v1587[2]);
                v250 = v1587[1];
                if ( v1587[1] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[1] - 4LL)) == 0 )
                  sub_1412EC9A0(a1: v250 - 4);
                v251 = v1587[0];
                if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] - 4LL)) == 0 )
                  sub_1412EC9A0(a1: v251 - 4);
                ++v246;
              }
              while ( v246 < (int)v1602 );
              a1 = (_QWORD *)v10;
LABEL_275:
              LOBYTE(v10) = v1604;
LABEL_276:
              v180 = v1595;
              if ( v1595 != nullptr && _InterlockedDecrement(v1595 + 2) == 0 )
                (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v180)(a1: v180, a2: 1);
              if ( (_BYTE)v1599 == 0 )
                goto LABEL_2928;
LABEL_280:
              if ( (v1605 & (unsigned __int8)(v10 & v1561)) == 0 )
                goto LABEL_381;
              v181 = *((_DWORD *)a1 + 92);
              v32 = (__int64)&v1583;
              sub_14080D0E0(a1: &v1583, a2: 0x1418E2C24LL);
              v1594 = v181;
              v1586 = 7;
              sub_1408085A0(a1: &v1600, a2: &v1586);
              sub_1408085A0(a1: &v1596, a2: &v1594);
              v1602 = nullptr;
              v182 = (int *)v1596;
              if ( v1596 != nullptr )
              {
                _InterlockedIncrement(v1596 - 1);
                v1602 = v182;
                v183 = *v182;
              }
              else
              {
                v183 = 0;
              }
              v223 = v183 + 1;
              v224 = sub_1412EC810(a1: 264, a2: (unsigned int)(v183 + 1));
              v225 = (volatile signed __int32 *)v224;
              *(_DWORD *)v224 = 0;
              v226 = 0;
              if ( v183 + 1 <= 0 )
                v223 = 0;
              *(_DWORD *)(v224 + 4) = v223;
              v227 = v224 + 8;
              *(_BYTE *)(v224 + 8) = 0;
              if ( v183 <= 0 )
              {
                v229 = (_BYTE *)(v224 + 8);
                if ( v183 == 0 )
                  goto LABEL_352;
              }
              else
              {
                v228 = 0x1419435F1LL;
                if ( v1602 != nullptr )
                  v228 = (__int64)(v1602 + 1);
                sub_141758A00(a1: v224 + 8, a2: v228, a3: (unsigned int)v183);
                v229 = (_BYTE *)(v227 + (unsigned int)v183);
LABEL_352:
                *v229 = 0;
                v226 = v183;
              }
              v230 = v224 + 4;
              *(_WORD *)(v227 + v226) = 95;
              v231 = v1602 - 1;
              if ( v1602 != nullptr && _InterlockedDecrement(v231) == 0 )
                sub_1412EC9A0(a1: v231);
              v1602 = nullptr;
              _InterlockedIncrement(v225);
              v1602 = (volatile signed __int32 *)v230;
              sub_140809550(a1: &v1602, a2: v1587, a3: &v1600);
              v1593 = 0;
              v232 = v1587[0];
              if ( v1587[0] != 0 )
              {
                _InterlockedIncrement((volatile signed __int32 *)(v1587[0] - 4LL));
                v233 = v1587[0];
                v1593 = v232;
                if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] - 4LL)) == 0 )
                  sub_1412EC9A0(a1: v233 - 4);
              }
              v234 = v1602;
              if ( v1602 != nullptr && _InterlockedDecrement(v1602 - 1) == 0 )
                sub_1412EC9A0(a1: v234 - 1);
              v235 = v1596;
              if ( v1596 != nullptr && _InterlockedDecrement(v1596 - 1) == 0 )
                sub_1412EC9A0(a1: v235 - 1);
              v236 = v1600;
              if ( v1600 != nullptr && _InterlockedDecrement(v1600 - 1) == 0 )
                sub_1412EC9A0(a1: v236 - 1);
              v1587[0] = 0x80100004E554C4CLL;
              LOBYTE(v1553) = 0;
              sub_1407D0F70(
                a1: (unsigned int)v1587,
                a2: (unsigned int)&v1595,
                a3: a2,
                a4: (unsigned int)&v1593,
                a5: (__int64)&v1583,
                a6: 0,
                a7: 0,
                v1553);
              v237 = v1593;
              if ( v1593 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1593 - 4)) == 0 )
                sub_1412EC9A0(a1: v237 - 4);
              v238 = v1595;
              if ( v1595 == nullptr )
                goto LABEL_2928;
              v239 = v1603[19] != v1603[18];
              LODWORD(v1602) = 0;
              (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **, __int64))(*(_QWORD *)v1595 + 40LL))(
                a1: v1595,
                a2: &v1602,
                a3: 4);
              if ( *((_DWORD *)v238 + 4) != 0 )
                goto LABEL_375;
              v240 = v1601;
              if ( v1601 != 0 )
              {
                LOBYTE(v240) = 1;
                if ( (int)v1602 <= 0 )
                  goto LABEL_376;
                v316 = 0;
                while ( 1 )
                {
                  v1587[0] = 0;
                  BYTE4(v1587[1]) = -1;
                  LODWORD(v1587[1]) = 0;
                  v317 = v1595;
                  if ( v1595 != nullptr )
                    _InterlockedIncrement(v1595 + 2);
                  (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *, __int64))(*(_QWORD *)v317 + 40LL))(
                    a1: v317,
                    a2: &v1587[1],
                    a3: 4);
                  if ( *((_DWORD *)v317 + 4) != 0 )
                    break;
                  sub_140814B10(a1: v317, a2: &v1600, a3: v1587);
                  if ( (_DWORD)v1600 != 0 )
                    break;
                  (*(void (__fastcall **)(volatile signed __int32 *, char *, __int64))(*(_QWORD *)v317 + 40LL))(
                    a1: v317,
                    a2: (char *)&v1587[1] + 4,
                    a3: 1);
                  v318 = *((_DWORD *)v317 + 4) == 0;
                  if ( _InterlockedDecrement(v317 + 2) == 0 )
                    goto LABEL_524;
LABEL_525:
                  if ( !v318 )
                  {
                    v1040 = v1587[0];
                    if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] - 4LL)) == 0 )
                      sub_1412EC9A0(a1: v1040 - 4);
LABEL_375:
                    LOBYTE(v240) = 0;
LABEL_376:
                    a1 = v1603;
                    LOBYTE(v10) = v1604;
LABEL_377:
                    v241 = v1595;
                    if ( v1595 != nullptr && _InterlockedDecrement(v1595 + 2) == 0 )
                      (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v241)(a1: v241, a2: 1);
                    if ( (_BYTE)v240 == 0 )
                      goto LABEL_2928;
LABEL_381:
                    if ( (v1605 & (unsigned __int8)(v10 & v1562)) == 0 )
                      goto LABEL_503;
                    v242 = *((_DWORD *)a1 + 92);
                    v32 = (__int64)&v1583;
                    sub_14080D0E0(a1: &v1583, a2: 0x1418E2C24LL);
                    LODWORD(v1597) = v242;
                    v1594 = v242;
                    v1586 = 35;
                    sub_1408085A0(a1: &v1600, a2: &v1586);
                    sub_1408085A0(a1: &v1596, a2: &v1594);
                    v1602 = nullptr;
                    v243 = (int *)v1596;
                    if ( v1596 != nullptr )
                    {
                      _InterlockedIncrement(v1596 - 1);
                      v1602 = v243;
                      v244 = *v243;
                    }
                    else
                    {
                      v244 = 0;
                    }
                    v10 = (__int64)a1;
                    v290 = v244 + 1;
                    v291 = sub_1412EC810(a1: 264, a2: (unsigned int)(v244 + 1));
                    v292 = (volatile signed __int32 *)v291;
                    *(_DWORD *)v291 = 0;
                    v293 = 0;
                    if ( v244 + 1 <= 0 )
                      v290 = 0;
                    *(_DWORD *)(v291 + 4) = v290;
                    v294 = v291 + 8;
                    *(_BYTE *)(v291 + 8) = 0;
                    if ( v244 <= 0 )
                    {
                      v296 = (_BYTE *)(v291 + 8);
                      if ( v244 == 0 )
                        goto LABEL_474;
                    }
                    else
                    {
                      v295 = 0x1419435F1LL;
                      if ( v1602 != nullptr )
                        v295 = (__int64)(v1602 + 1);
                      sub_141758A00(a1: v291 + 8, a2: v295, a3: (unsigned int)v244);
                      v296 = (_BYTE *)(v294 + (unsigned int)v244);
LABEL_474:
                      *v296 = 0;
                      v293 = v244;
                    }
                    v297 = v291 + 4;
                    *(_WORD *)(v294 + v293) = 95;
                    v298 = v1602 - 1;
                    if ( v1602 != nullptr && _InterlockedDecrement(v298) == 0 )
                      sub_1412EC9A0(a1: v298);
                    v1602 = nullptr;
                    _InterlockedIncrement(v292);
                    v1602 = (volatile signed __int32 *)v297;
                    sub_140809550(a1: &v1602, a2: v1587, a3: &v1600);
                    v1593 = 0;
                    v299 = v1587[0];
                    if ( v1587[0] != 0 )
                    {
                      _InterlockedIncrement((volatile signed __int32 *)(v1587[0] - 4LL));
                      v300 = v1587[0];
                      v1593 = v299;
                      if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] - 4LL)) == 0 )
                        sub_1412EC9A0(a1: v300 - 4);
                    }
                    v301 = v1602;
                    a1 = (_QWORD *)v10;
                    if ( v1602 != nullptr && _InterlockedDecrement(v1602 - 1) == 0 )
                      sub_1412EC9A0(a1: v301 - 1);
                    v302 = v1596;
                    if ( v1596 != nullptr && _InterlockedDecrement(v1596 - 1) == 0 )
                      sub_1412EC9A0(a1: v302 - 1);
                    v303 = v1600;
                    if ( v1600 != nullptr && _InterlockedDecrement(v1600 - 1) == 0 )
                      sub_1412EC9A0(a1: v303 - 1);
                    v1587[0] = 0x80100004E554C4CLL;
                    LOBYTE(v1553) = 0;
                    sub_1407D0F70(
                      a1: (unsigned int)v1587,
                      a2: (unsigned int)&v1595,
                      a3: a2,
                      a4: (unsigned int)&v1593,
                      a5: (__int64)&v1583,
                      a6: 0,
                      a7: 0,
                      v1553);
                    v304 = v1593;
                    if ( v1593 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1593 - 4)) == 0 )
                      sub_1412EC9A0(a1: v304 - 4);
                    v305 = v1595;
                    if ( v1595 == nullptr )
                      goto LABEL_2928;
                    v306 = *(_QWORD *)(v10 + 296) != *(_QWORD *)(v10 + 288);
                    LODWORD(v1602) = 0;
                    (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **, __int64))(*(_QWORD *)v1595 + 40LL))(
                      a1: v1595,
                      a2: &v1602,
                      a3: 4);
                    if ( *((_DWORD *)v305 + 4) != 0 )
                    {
                      LODWORD(v1599) = 0;
                      goto LABEL_498;
                    }
                    LODWORD(v439) = (_DWORD)v1602;
                    if ( v1601 != 0 )
                    {
                      LOBYTE(v307) = 1;
                      LODWORD(v1599) = v307;
                      if ( (int)v1602 > 0 )
                      {
                        v440 = 0;
                        v32 = (__int64)v1587;
                        v441 = v1597;
                        while ( 1 )
                        {
                          WORD2(v1587[0]) = -1;
                          v1587[1] = 0;
                          LODWORD(v1587[0]) = 0;
                          v1600 = v1595;
                          if ( v1595 != nullptr )
                            _InterlockedIncrement(v1595 + 2);
                          v442 = sub_14159B8E0(a1: v1587, a2: &v1600, a3: v441);
                          v443 = v1600;
                          if ( v1600 != nullptr && _InterlockedDecrement(v1600 + 2) == 0 )
                            (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v443)(a1: v443, a2: 1);
                          if ( v442 == 0 )
                            break;
                          v444 = sub_140F74650(a1: qword_141B5FE18, a2: LODWORD(v1587[0]));
                          if ( v444 != 0 )
                          {
                            *(_WORD *)(v444 + 32) = WORD2(v1587[0]);
                            sub_140E45B70(a1: v444 + 24, a2: &v1587[1]);
                          }
                          sub_140E44A40(a1: &v1587[1]);
                          if ( ++v440 >= (int)v1602 )
                            goto LABEL_2228;
                        }
                        sub_140E44A40(a1: &v1587[1]);
                        LODWORD(v1599) = 0;
LABEL_2228:
                        a1 = (_QWORD *)v10;
                      }
LABEL_498:
                      LOBYTE(v10) = v1604;
LABEL_499:
                      v308 = v1595;
                      if ( v1595 != nullptr && _InterlockedDecrement(v1595 + 2) == 0 )
                        (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v308)(a1: v308, a2: 1);
                      if ( (_BYTE)v1599 == 0 )
                        goto LABEL_2928;
LABEL_503:
                      if ( (a9 & (unsigned __int8)(v10 & v1563)) == 0 )
                        goto LABEL_735;
                      v309 = *((_DWORD *)a1 + 92);
                      v32 = (__int64)&v1583;
                      sub_14080D0E0(a1: &v1583, a2: 0x1418E2C24LL);
                      LODWORD(v1597) = v309;
                      v1594 = v309;
                      v1586 = 6;
                      sub_1408085A0(a1: &v1600, a2: &v1586);
                      sub_1408085A0(a1: &v1596, a2: &v1594);
                      v1602 = nullptr;
                      v310 = (int *)v1596;
                      if ( v1596 != nullptr )
                      {
                        _InterlockedIncrement(v1596 - 1);
                        v1602 = v310;
                        v311 = *v310;
                      }
                      else
                      {
                        v311 = 0;
                      }
                      v10 = (__int64)a1;
                      v408 = v311 + 1;
                      v409 = sub_1412EC810(a1: 264, a2: (unsigned int)(v311 + 1));
                      v410 = (volatile signed __int32 *)v409;
                      *(_DWORD *)v409 = 0;
                      v411 = 0;
                      if ( v311 + 1 <= 0 )
                        v408 = 0;
                      *(_DWORD *)(v409 + 4) = v408;
                      v412 = v409 + 8;
                      *(_BYTE *)(v409 + 8) = 0;
                      if ( v311 <= 0 )
                      {
                        v414 = (_BYTE *)(v409 + 8);
                        if ( v311 == 0 )
                          goto LABEL_706;
                      }
                      else
                      {
                        v413 = 0x1419435F1LL;
                        if ( v1602 != nullptr )
                          v413 = (__int64)(v1602 + 1);
                        sub_141758A00(a1: v409 + 8, a2: v413, a3: (unsigned int)v311);
                        v414 = (_BYTE *)(v412 + (unsigned int)v311);
LABEL_706:
                        *v414 = 0;
                        v411 = v311;
                      }
                      v415 = v409 + 4;
                      *(_WORD *)(v412 + v411) = 95;
                      v416 = v1602 - 1;
                      if ( v1602 != nullptr && _InterlockedDecrement(v416) == 0 )
                        sub_1412EC9A0(a1: v416);
                      v1602 = nullptr;
                      _InterlockedIncrement(v410);
                      v1602 = (volatile signed __int32 *)v415;
                      sub_140809550(a1: &v1602, a2: v1587, a3: &v1600);
                      v1593 = 0;
                      v417 = v1587[0];
                      if ( v1587[0] != 0 )
                      {
                        _InterlockedIncrement((volatile signed __int32 *)(v1587[0] - 4LL));
                        v418 = v1587[0];
                        v1593 = v417;
                        if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] - 4LL)) == 0 )
                          sub_1412EC9A0(a1: v418 - 4);
                      }
                      v419 = v1602;
                      a1 = (_QWORD *)v10;
                      if ( v1602 != nullptr && _InterlockedDecrement(v1602 - 1) == 0 )
                        sub_1412EC9A0(a1: v419 - 1);
                      v420 = v1596;
                      if ( v1596 != nullptr && _InterlockedDecrement(v1596 - 1) == 0 )
                        sub_1412EC9A0(a1: v420 - 1);
                      v421 = v1600;
                      if ( v1600 != nullptr && _InterlockedDecrement(v1600 - 1) == 0 )
                        sub_1412EC9A0(a1: v421 - 1);
                      v1587[0] = 0x80100004E554C4CLL;
                      LOBYTE(v1553) = 0;
                      sub_1407D0F70(
                        a1: (unsigned int)v1587,
                        a2: (unsigned int)&v1595,
                        a3: a2,
                        a4: (unsigned int)&v1593,
                        a5: (__int64)&v1583,
                        a6: 0,
                        a7: 0,
                        v1553);
                      v422 = v1593;
                      if ( v1593 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1593 - 4)) == 0 )
                        sub_1412EC9A0(a1: v422 - 4);
                      v423 = v1595;
                      if ( v1595 == nullptr )
                        goto LABEL_2928;
                      v424 = *(_QWORD *)(v10 + 128) != *(_QWORD *)(v10 + 120);
                      LODWORD(v1602) = 0;
                      (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **, __int64))(*(_QWORD *)v1595 + 40LL))(
                        a1: v1595,
                        a2: &v1602,
                        a3: 4);
                      if ( *((_DWORD *)v423 + 4) != 0 )
                        goto LABEL_729;
                      LODWORD(v646) = (_DWORD)v1602;
                      if ( v1601 != 0 )
                      {
                        LOBYTE(v425) = 1;
                        LODWORD(v1599) = v425;
                        if ( (int)v1602 > 0 )
                        {
                          v647 = 0;
                          v32 = (__int64)&v1587[2];
                          v648 = v1597;
                          while ( 1 )
                          {
                            memset(v1587, 0, 28);
                            WORD2(v1587[3]) = -1;
                            v1600 = v1595;
                            if ( v1595 != nullptr )
                              _InterlockedIncrement(v1595 + 2);
                            v649 = sub_140E498B0(a1: v1587, a2: &v1600, a3: v648);
                            v650 = v1600;
                            if ( v1600 != nullptr && _InterlockedDecrement(v1600 + 2) == 0 )
                              (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v650)(a1: v650, a2: 1);
                            if ( v649 == 0 )
                              break;
                            sub_141582B80(a1: v1587);
                            sub_140E44A40(a1: &v1587[2]);
                            v651 = v1587[1];
                            if ( v1587[1] != 0
                              && _InterlockedDecrement((volatile signed __int32 *)(v1587[1] - 4LL)) == 0 )
                            {
                              sub_1412EC9A0(a1: v651 - 4);
                            }
                            v652 = v1587[0];
                            if ( v1587[0] != 0
                              && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] - 4LL)) == 0 )
                            {
                              sub_1412EC9A0(a1: v652 - 4);
                            }
                            if ( ++v647 >= (int)v1602 )
                            {
                              a1 = (_QWORD *)v10;
                              goto LABEL_730;
                            }
                          }
                          sub_140E44A40(a1: &v1587[2]);
                          v1216 = v1587[1];
                          if ( v1587[1] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[1] - 4LL)) == 0 )
                            sub_1412EC9A0(a1: v1216 - 4);
                          v1217 = v1587[0];
                          a1 = (_QWORD *)v10;
                          if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] - 4LL)) == 0 )
                            sub_1412EC9A0(a1: v1217 - 4);
LABEL_729:
                          LODWORD(v1599) = 0;
                        }
LABEL_730:
                        LOBYTE(v10) = v1604;
LABEL_731:
                        v426 = v1595;
                        if ( v1595 != nullptr && _InterlockedDecrement(v1595 + 2) == 0 )
                          (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v426)(a1: v426, a2: 1);
                        if ( (_BYTE)v1599 == 0 )
                          goto LABEL_2928;
LABEL_735:
                        v1605 &= v1565 & (unsigned __int8)v10;
                        if ( v1605 == 0 )
                          goto LABEL_1159;
                        v1604 = *((_DWORD *)a1 + 92);
                        v427 = v1604;
                        v32 = (__int64)&v1583;
                        sub_14080D0E0(a1: &v1583, a2: 0x1418E2C24LL);
                        v1594 = v427;
                        v1586 = 18;
                        sub_1408085A0(a1: &v1600, a2: &v1586);
                        sub_1408085A0(a1: &v1596, a2: &v1594);
                        v1602 = nullptr;
                        v428 = (int *)v1596;
                        if ( v1596 != nullptr )
                        {
                          _InterlockedIncrement(v1596 - 1);
                          v1602 = v428;
                          v429 = *v428;
                        }
                        else
                        {
                          v429 = 0;
                        }
                        v616 = a1;
                        v617 = v429 + 1;
                        v618 = sub_1412EC810(a1: 264, a2: (unsigned int)(v429 + 1));
                        v619 = (volatile signed __int32 *)v618;
                        *(_DWORD *)v618 = 0;
                        v620 = 0;
                        if ( v429 + 1 <= 0 )
                          v617 = 0;
                        *(_DWORD *)(v618 + 4) = v617;
                        v621 = v618 + 8;
                        *(_BYTE *)(v618 + 8) = 0;
                        if ( v429 <= 0 )
                        {
                          v623 = (_BYTE *)(v618 + 8);
                          if ( v429 == 0 )
                            goto LABEL_1131;
                        }
                        else
                        {
                          v622 = 0x1419435F1LL;
                          if ( v1602 != nullptr )
                            v622 = (__int64)(v1602 + 1);
                          sub_141758A00(a1: v618 + 8, a2: v622, a3: (unsigned int)v429);
                          v623 = (_BYTE *)(v621 + (unsigned int)v429);
LABEL_1131:
                          *v623 = 0;
                          v620 = v429;
                        }
                        v624 = v618 + 4;
                        *(_WORD *)(v621 + v620) = 95;
                        v625 = v1602 - 1;
                        if ( v1602 != nullptr && _InterlockedDecrement(v625) == 0 )
                          sub_1412EC9A0(a1: v625);
                        v1602 = nullptr;
                        _InterlockedIncrement(v619);
                        v1602 = (volatile signed __int32 *)v624;
                        sub_140809550(a1: &v1602, a2: v1587, a3: &v1600);
                        v1593 = 0;
                        v626 = v1587[0];
                        if ( v1587[0] != 0 )
                        {
                          _InterlockedIncrement((volatile signed __int32 *)(v1587[0] - 4LL));
                          v627 = v1587[0];
                          v1593 = v626;
                          if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] - 4LL)) == 0 )
                            sub_1412EC9A0(a1: v627 - 4);
                        }
                        v628 = v1602;
                        if ( v1602 != nullptr && _InterlockedDecrement(v1602 - 1) == 0 )
                          sub_1412EC9A0(a1: v628 - 1);
                        v629 = v1596;
                        if ( v1596 != nullptr && _InterlockedDecrement(v1596 - 1) == 0 )
                          sub_1412EC9A0(a1: v629 - 1);
                        v630 = v1600;
                        if ( v1600 != nullptr && _InterlockedDecrement(v1600 - 1) == 0 )
                          sub_1412EC9A0(a1: v630 - 1);
                        v1587[0] = 0x80100004E554C4CLL;
                        LOBYTE(v1553) = 0;
                        sub_1407D0F70(
                          a1: (unsigned int)v1587,
                          a2: (unsigned int)&v1595,
                          a3: a2,
                          a4: (unsigned int)&v1593,
                          a5: (__int64)&v1583,
                          a6: 0,
                          a7: 0,
                          v1553);
                        v631 = v1593;
                        if ( v1593 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1593 - 4)) == 0 )
                          sub_1412EC9A0(a1: v631 - 4);
                        v632 = v1595;
                        if ( v1595 != nullptr )
                        {
                          v633 = v616[40] != v616[39];
                          LODWORD(v1602) = 0;
                          (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **, __int64))(*(_QWORD *)v1595 + 40LL))(
                            a1: v1595,
                            a2: &v1602,
                            a3: 4);
                          if ( *((_DWORD *)v632 + 4) != 0 )
                            goto LABEL_1154;
                          if ( v1601 != 0 )
                          {
                            v634 = 1;
                            if ( (int)v1602 > 0 )
                            {
                              v826 = 0;
                              v32 = (__int64)&v1600;
                              v827 = v1604;
                              while ( 1 )
                              {
                                memset(v1587, 0, sizeof(v1587));
                                *(_QWORD *)&v1588 = 0;
                                *((_QWORD *)&v1588 + 1) = 0xFFFFFFFF00000000uLL;
                                v1600 = v1595;
                                if ( v1595 != nullptr )
                                  _InterlockedIncrement(v1595 + 2);
                                v828 = sub_140FFFC00(a1: v1587, a2: &v1600, a3: v827);
                                v829 = v1600;
                                if ( v1600 != nullptr && _InterlockedDecrement(v1600 + 2) == 0 )
                                  (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v829)(a1: v829, a2: 1);
                                if ( v828 == 0 )
                                  break;
                                sub_140FFFA20(a1: v1587);
                                sub_140E44A40(a1: &v1588);
                                v830 = v1587[3];
                                if ( v1587[3] != 0
                                  && _InterlockedDecrement((volatile signed __int32 *)(v1587[3] - 4LL)) == 0 )
                                {
                                  sub_1412EC9A0(a1: v830 - 4);
                                }
                                v831 = v1587[2];
                                if ( v1587[2] != 0
                                  && _InterlockedDecrement((volatile signed __int32 *)(v1587[2] - 4LL)) == 0 )
                                {
                                  sub_1412EC9A0(a1: v831 - 4);
                                }
                                v832 = v1587[1];
                                if ( v1587[1] != 0
                                  && _InterlockedDecrement((volatile signed __int32 *)(v1587[1] - 4LL)) == 0 )
                                {
                                  sub_1412EC9A0(a1: v832 - 4);
                                }
                                v833 = v1587[0];
                                if ( v1587[0] != 0
                                  && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] - 4LL)) == 0 )
                                {
                                  sub_1412EC9A0(a1: v833 - 4);
                                }
                                if ( ++v826 >= (int)v1602 )
                                  goto LABEL_2383;
                              }
                              sub_140E44A40(a1: &v1588);
                              v1356 = v1587[3];
                              if ( v1587[3] != 0
                                && _InterlockedDecrement((volatile signed __int32 *)(v1587[3] - 4LL)) == 0 )
                              {
                                sub_1412EC9A0(a1: v1356 - 4);
                              }
                              v1357 = v1587[2];
                              if ( v1587[2] != 0
                                && _InterlockedDecrement((volatile signed __int32 *)(v1587[2] - 4LL)) == 0 )
                              {
                                sub_1412EC9A0(a1: v1357 - 4);
                              }
                              v1358 = v1587[1];
                              if ( v1587[1] != 0
                                && _InterlockedDecrement((volatile signed __int32 *)(v1587[1] - 4LL)) == 0 )
                              {
                                sub_1412EC9A0(a1: v1358 - 4);
                              }
                              v1359 = v1587[0];
                              if ( v1587[0] != 0
                                && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] - 4LL)) == 0 )
                              {
                                sub_1412EC9A0(a1: v1359 - 4);
                              }
LABEL_1154:
                              v634 = 0;
                            }
LABEL_1155:
                            v635 = v1595;
                            if ( v1595 != nullptr && _InterlockedDecrement(v1595 + 2) == 0 )
                              (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v635)(a1: v635, a2: 1);
                            if ( v634 != 0 )
                            {
LABEL_1159:
                              v636 = qword_141B59FA0;
                              if ( qword_141B59FA0 != 0 && v1581 != 0 )
                              {
                                v637 = v1580;
                                v638 = (unsigned int)MEMORY[0x141947498]();
                                v639 = *(_QWORD *)(v636 + 16);
                                if ( v639 == 0 || v639 == (unsigned int)v638 )
                                {
                                  if ( v637 == 0 )
                                    v638 = 0;
                                  *(_QWORD *)(v636 + 16) = v638;
                                }
                                *(_QWORD *)(v636 + 8) = v1579;
                              }
                              LOBYTE(v32) = 1;
                              return (unsigned int)v32;
                            }
                            goto LABEL_2928;
                          }
                          v1055 = (int)v1602;
                          v1056 = v633;
                          if ( v633 )
                          {
                            v1057 = v616[39];
                            v1058 = (v616[40] - v1057) >> 3;
                            v1059 = v1058 + (int)v1602;
                            v1060 = (v616[41] - v1057) >> 3;
                            if ( v1060 < v1059 )
                            {
                              if ( v1059 >> 61 == 0 )
                              {
                                v32 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v1059);
                                v1061 = v616;
                                sub_141758A00(a1: v32, a2: v616[39], a3: v616[40] - v616[39]);
                                if ( v616[39] != 0 )
                                  sub_1407E4890(a1: qword_141ABD470);
                                v616[39] = v32;
                                v616[40] = v32 + 8 * v1058;
                                v1062 = v32 + 8 * v1059;
                                goto LABEL_2379;
                              }
LABEL_3124:
                              sub_1400526C0(a1: v1060);
                            }
                          }
                          else
                          {
                            v32 = v616[39];
                            v1060 = (v616[41] - v32) >> 3;
                            if ( v1060 < (int)v1602 )
                            {
                              if ( (int)v1602 < 0 )
                                goto LABEL_3124;
                              v1061 = v616;
                              v1212 = v616[40];
                              v1213 = sub_1407E4490(a1: qword_141ABD470, a2: 8LL * (int)v1602);
                              sub_141758A00(a1: v1213, a2: v616[39], a3: v616[40] - v616[39]);
                              if ( v616[39] != 0 )
                                sub_1407E4890(a1: qword_141ABD470);
                              v616[39] = v1213;
                              v616[40] = v1213 + v1212 - v32;
                              v1062 = v1213 + 8 * v1055;
LABEL_2379:
                              v1061[41] = v1062;
                            }
                          }
                          if ( (int)v1602 <= 0 )
                          {
LABEL_2383:
                            v634 = 1;
                            goto LABEL_1155;
                          }
                          if ( !v1056 )
                          {
                            v1360 = 0;
                            v32 = (__int64)v616;
                            v1361 = v1604;
                            do
                            {
                              if ( dword_141B60810 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer
                                                                 + (unsigned int)TlsIndex)
                                                               + 4LL) )
                              {
                                sub_141750E08(a1: &dword_141B60810);
                                if ( dword_141B60810 == -1 )
                                {
                                  sub_1407E53D0(
                                    a1: (unsigned int)&unk_141B607C0,
                                    a2: 1100150588,
                                    a3: 1024,
                                    a4: 48,
                                    a5: 0,
                                    a6: 1,
                                    a7: 1024,
                                    a8: 4096);
                                  sub_141751048(a1: sub_140FE1280);
                                  sub_141750EA0(a1: &dword_141B60810);
                                }
                              }
                              v1362 = (_QWORD *)sub_1407E58C0(a1: &unk_141B607C0, a2: 48);
                              *v1362 = 0;
                              v1362[1] = 0;
                              v1362[2] = 0;
                              v1362[3] = 0;
                              v1362[4] = 0;
                              v1362[5] = 0xFFFFFFFF00000000uLL;
                              v1587[0] = v1595;
                              if ( v1595 != nullptr )
                                _InterlockedIncrement(v1595 + 2);
                              v634 = sub_140FFFC00(a1: v1362, a2: v1587, a3: v1361);
                              v1363 = (void (__fastcall ***)(_QWORD, __int64))v1587[0];
                              if ( v1587[0] != 0
                                && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] + 8LL)) == 0 )
                              {
                                (**v1363)(a1: v1363, a2: 1);
                              }
                              if ( v634 == 0 )
                                break;
                              v1364 = *(_QWORD **)(v32 + 320);
                              if ( v1364 == *(_QWORD **)(v32 + 328) )
                              {
                                LODWORD(v1597) = v1360;
                                v1572 = v634;
                                v1365 = (__int64)v1364 - *(_QWORD *)(v32 + 312);
                                v1366 = v1365 >> 3;
                                v1367 = (unsigned __int64)(v1365 >> 3) >> 1;
                                v1368 = 0x1FFFFFFFFFFFFFFFLL - v1367;
                                v1369 = (v1365 >> 3) + v1367;
                                v1599 = (v1365 >> 3) + 1;
                                if ( v1369 <= v1599 )
                                  v1369 = v1366 + 1;
                                if ( v1366 > v1368 )
                                  v1369 = 0x1FFFFFFFFFFFFFFFLL;
                                v1370 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v1369);
                                *(_QWORD *)(v1370 + v1365) = v1362;
                                v1371 = *(_QWORD **)(v32 + 320);
                                sub_141758A00(
                                  a1: v1370,
                                  a2: *(_QWORD *)(v32 + 312),
                                  a3: (char *)v1364 - *(_QWORD *)(v32 + 312));
                                if ( v1371 != v1364 )
                                  sub_141758A00(
                                    a1: v1370 + v1365 + 8,
                                    a2: v1364,
                                    a3: *(_QWORD *)(v32 + 320) - (_QWORD)v1364);
                                v1372 = v1370;
                                v1373 = *(_QWORD *)(v32 + 312);
                                v1374 = (_QWORD *)v32;
                                v1361 = v1604;
                                v1360 = v1597;
                                if ( v1373 != 0 )
                                {
                                  v1375 = *(_QWORD *)(v32 + 328) - v1373;
                                  if ( v1375 == -1 )
                                    v1375 = *(unsigned int *)(v1373 - *(unsigned int *)(qword_141ABD470 + 48));
                                  if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                                    && (v1376 = *(_QWORD *)(qword_141ABD470 + 24),
                                        (*(_QWORD *)(qword_141ABD470 + 32) - v1376) >> 3 > v1375)
                                    && (v1377 = *(_QWORD *)(v1376 + 8 * v1375)) != 0 )
                                  {
                                    MEMORY[0x1419475D8](a1: v1377 + 32, a2: v1373 - *(unsigned int *)(v1377 + 120));
                                    v1378 = *(_BYTE *)(v1377 + 72) != 0
                                         && _InterlockedDecrement((volatile signed __int32 *)(v1377 + 64)) != 0;
                                    v1374 = v1603;
                                    if ( !v1378 && *(_BYTE *)(v1377 + 97) != 0 )
                                      sub_1412D33C0(a1: v1377);
                                  }
                                  else
                                  {
                                    MEMORY[0x141948990](a1: v1373 - *(unsigned int *)(qword_141ABD470 + 48));
                                    v1374 = v1603;
                                  }
                                }
                                v1374[39] = v1372;
                                v1374[40] = v1372 + 8 * v1599;
                                v1374[41] = v1372 + 8 * v1369;
                                v32 = (__int64)v1374;
                                v634 = v1572;
                              }
                              else
                              {
                                *v1364 = v1362;
                                *(_QWORD *)(v32 + 320) += 8LL;
                              }
                              ++v1360;
                            }
                            while ( v1360 < (int)v1602 );
                            goto LABEL_1155;
                          }
                          v1214 = 0;
                          v32 = (__int64)v616;
                          v1215 = v1604;
                          while ( 2 )
                          {
                            if ( dword_141B60810 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer
                                                               + (unsigned int)TlsIndex)
                                                             + 4LL) )
                            {
                              sub_141750E08(a1: &dword_141B60810);
                              if ( dword_141B60810 == -1 )
                              {
                                sub_1407E53D0(
                                  a1: (unsigned int)&unk_141B607C0,
                                  a2: 1100150588,
                                  a3: 1024,
                                  a4: 48,
                                  a5: 0,
                                  a6: 1,
                                  a7: 1024,
                                  a8: 4096);
                                sub_141751048(a1: sub_140FE1280);
                                sub_141750EA0(a1: &dword_141B60810);
                              }
                            }
                            v1287 = (_QWORD *)sub_1407E58C0(a1: &unk_141B607C0, a2: 48);
                            *v1287 = 0;
                            v1287[1] = 0;
                            v1287[2] = 0;
                            v1287[3] = 0;
                            v1287[4] = 0;
                            v1287[5] = 0xFFFFFFFF00000000uLL;
                            v1587[0] = v1595;
                            if ( v1595 != nullptr )
                              _InterlockedIncrement(v1595 + 2);
                            v1288 = sub_140FFFC00(a1: v1287, a2: v1587, a3: v1215);
                            v1289 = (void (__fastcall ***)(_QWORD, __int64))v1587[0];
                            if ( v1587[0] != 0
                              && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] + 8LL)) == 0 )
                            {
                              (**v1289)(a1: v1289, a2: 1);
                            }
                            if ( v1288 == 0 )
                              goto LABEL_1154;
                            LODWORD(v1599) = v1214;
                            v1571 = v1288;
                            v1290 = *(_QWORD *)(v32 + 312);
                            v1291 = *(_QWORD **)(v32 + 320);
                            v1292 = (__int64)v1291 - v1290;
                            v1293 = (_QWORD *)v1290;
                            if ( (__int64)v1291 - v1290 > 0 )
                            {
                              v1294 = (unsigned __int64)v1292 >> 3;
                              v1293 = *(_QWORD **)(v32 + 312);
                              v1295 = (unsigned __int64)v1292 >> 3;
                              do
                              {
                                v1295 = (unsigned __int64)v1295 >> 1;
                                if ( *(_DWORD *)(v1293[v1295] + 40LL) < *((_DWORD *)v1287 + 10) )
                                {
                                  v1293 += v1295 + 1;
                                  v1295 = v1294 + ~v1295;
                                }
                                v1294 = v1295;
                              }
                              while ( v1295 > 0 );
                            }
                            if ( v1293 == v1291 )
                            {
                              v32 = (__int64)v1603;
                              if ( v1291 == (_QWORD *)v1603[41] )
                              {
                                v1316 = (unsigned __int64)(v1292 >> 3) >> 1;
                                v1317 = 0x1FFFFFFFFFFFFFFFLL - v1316;
                                v1318 = (v1292 >> 3) + v1316;
                                v1597 = (v1292 >> 3) + 1;
                                if ( v1318 <= v1597 )
                                  v1318 = (v1292 >> 3) + 1;
                                if ( v1292 >> 3 > v1317 )
                                  v1318 = 0x1FFFFFFFFFFFFFFFLL;
                                v1319 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v1318);
                                *(_QWORD *)(v1319 + v1292) = v1287;
                                v1320 = v1319;
                                v1321 = *(_QWORD **)(v32 + 320);
                                sub_141758A00(
                                  a1: v1319,
                                  a2: *(_QWORD *)(v32 + 312),
                                  a3: (char *)v1291 - *(_QWORD *)(v32 + 312));
                                if ( v1321 != v1291 )
                                  sub_141758A00(
                                    a1: v1320 + v1292 + 8,
                                    a2: v1291,
                                    a3: *(_QWORD *)(v32 + 320) - (_QWORD)v1291);
                                v1322 = *(_QWORD *)(v32 + 312);
                                v1215 = v1604;
                                if ( v1322 != 0 )
                                {
                                  v1323 = *(_QWORD *)(v32 + 328) - v1322;
                                  if ( v1323 == -1 )
                                    v1323 = *(unsigned int *)(v1322 - *(unsigned int *)(qword_141ABD470 + 48));
                                  if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                                    && (v1324 = *(_QWORD *)(qword_141ABD470 + 24),
                                        (*(_QWORD *)(qword_141ABD470 + 32) - v1324) >> 3 > v1323)
                                    && (v1325 = *(_QWORD *)(v1324 + 8 * v1323)) != 0 )
                                  {
                                    MEMORY[0x1419475D8](a1: v1325 + 32, a2: v1322 - *(unsigned int *)(v1325 + 120));
                                    v1326 = *(_BYTE *)(v1325 + 72) != 0
                                         && _InterlockedDecrement((volatile signed __int32 *)(v1325 + 64)) != 0;
                                    if ( !v1326 && *(_BYTE *)(v1325 + 97) != 0 )
                                      sub_1412D33C0(a1: v1325);
                                  }
                                  else
                                  {
                                    MEMORY[0x141948990](a1: v1322 - *(unsigned int *)(qword_141ABD470 + 48));
                                  }
                                }
                                *(_QWORD *)(v32 + 312) = v1320;
                                *(_QWORD *)(v32 + 320) = v1320 + 8 * v1597;
                                *(_QWORD *)(v32 + 328) = v1320 + 8 * v1318;
                                goto LABEL_2542;
                              }
                              *v1291 = v1287;
                            }
                            else
                            {
                              v1296 = ((__int64)v1293 - v1290) >> 3;
                              if ( *(_DWORD *)(*v1293 + 40LL) == *((_DWORD *)v1287 + 10) )
                              {
                                v1297 = v1292 >> 3;
                                if ( v1297 > v1296 )
                                {
                                  v1298 = *(__int64 **)(v1290 + 8 * v1296);
                                  if ( v1298 != nullptr )
                                  {
                                    sub_140E44A40(a1: v1298 + 4);
                                    v1299 = v1298[3];
                                    if ( v1299 != 0
                                      && _InterlockedDecrement((volatile signed __int32 *)(v1299 - 4)) == 0 )
                                    {
                                      sub_1412EC9A0(a1: v1299 - 4);
                                    }
                                    v1300 = v1298[2];
                                    v1301 = v1603;
                                    if ( v1300 != 0
                                      && _InterlockedDecrement((volatile signed __int32 *)(v1300 - 4)) == 0 )
                                    {
                                      sub_1412EC9A0(a1: v1300 - 4);
                                    }
                                    v1302 = v1298[1];
                                    if ( v1302 != 0
                                      && _InterlockedDecrement((volatile signed __int32 *)(v1302 - 4)) == 0 )
                                    {
                                      sub_1412EC9A0(a1: v1302 - 4);
                                    }
                                    v1303 = *v1298;
                                    if ( *v1298 != 0
                                      && _InterlockedDecrement((volatile signed __int32 *)(v1303 - 4)) == 0 )
                                    {
                                      sub_1412EC9A0(a1: v1303 - 4);
                                    }
                                    sub_140FE1120(a1: v1298);
                                    v1290 = v1301[39];
                                    v1291 = (_QWORD *)v1301[40];
                                    v1297 = ((__int64)v1291 - v1290) >> 3;
                                  }
                                }
                                if ( v1297 <= v1296 )
                                {
                                  v1304 = v1296 + 1;
                                  v1305 = v1296 + 1 - v1297;
                                  if ( v1296 + 1 < v1297 )
                                  {
                                    v1603[40] = v1290 + 8 * v1304;
                                  }
                                  else if ( v1296 + 1 > v1297 )
                                  {
                                    v1306 = (v1603[41] - v1290) >> 3;
                                    if ( v1306 >= v1304 )
                                    {
                                      v1337 = v1603;
                                      sub_141758A10(a1: v1291, a2: 0, a3: 8 * v1305);
                                      v1337[40] = &v1291[v1305];
                                      v1290 = v1337[39];
                                    }
                                    else
                                    {
                                      v1060 = v1304 >> 61;
                                      if ( v1304 >> 61 != 0 )
                                        goto LABEL_3124;
                                      v1307 = v1306 + (v1306 >> 1);
                                      v1597 = v1296 + 1;
                                      if ( v1307 <= v1304 )
                                        v1307 = v1296 + 1;
                                      if ( v1306 > 0x1FFFFFFFFFFFFFFFLL - (v1306 >> 1) )
                                        v1307 = 0x1FFFFFFFFFFFFFFFLL;
                                      v1290 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v1307);
                                      sub_141758A10(a1: v1290 + 8 * v1297, a2: 0, a3: 8 * v1305);
                                      v1308 = v1603;
                                      sub_141758A00(a1: v1290, a2: v1603[39], a3: v1603[40] - v1603[39]);
                                      v1309 = v1308[39];
                                      if ( v1309 != 0 )
                                      {
                                        v1310 = v1308[41] - v1309;
                                        if ( v1310 == -1 )
                                          v1310 = *(unsigned int *)(v1309 - *(unsigned int *)(qword_141ABD470 + 48));
                                        if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                                          && (v1311 = *(_QWORD *)(qword_141ABD470 + 24),
                                              (*(_QWORD *)(qword_141ABD470 + 32) - v1311) >> 3 > v1310)
                                          && (v1312 = *(_QWORD *)(v1311 + 8 * v1310)) != 0 )
                                        {
                                          MEMORY[0x1419475D8](
                                            a1: v1312 + 32,
                                            a2: v1309 - *(unsigned int *)(v1312 + 120));
                                          v1313 = *(_BYTE *)(v1312 + 72) != 0
                                               && _InterlockedDecrement((volatile signed __int32 *)(v1312 + 64)) != 0;
                                          v1308 = v1603;
                                          if ( !v1313 && *(_BYTE *)(v1312 + 97) != 0 )
                                            sub_1412D33C0(a1: v1312);
                                        }
                                        else
                                        {
                                          MEMORY[0x141948990](a1: v1309 - *(unsigned int *)(qword_141ABD470 + 48));
                                          v1308 = v1603;
                                        }
                                      }
                                      v1308[39] = v1290;
                                      v1308[40] = v1290 + 8 * v1597;
                                      v1308[41] = v1290 + 8 * v1307;
                                    }
                                  }
                                }
                                *(_QWORD *)(v1290 + 8 * v1296) = v1287;
                                v32 = (__int64)v1603;
LABEL_2541:
                                v1215 = v1604;
LABEL_2542:
                                v1214 = v1599 + 1;
                                v634 = v1571;
                                if ( (int)v1599 + 1 >= (int)v1602 )
                                  goto LABEL_1155;
                                continue;
                              }
                              v1314 = (char *)(v1290 + 8 * v1296);
                              v1315 = v1603;
                              if ( v1291 == (_QWORD *)v1603[41] )
                              {
                                v1327 = v1292 >> 3;
                                v1328 = v1327 + (v1327 >> 1);
                                v1597 = v1327 + 1;
                                if ( v1328 <= v1327 + 1 )
                                  v1328 = v1327 + 1;
                                if ( v1327 > 0x1FFFFFFFFFFFFFFFLL - (v1327 >> 1) )
                                  v1328 = 0x1FFFFFFFFFFFFFFFLL;
                                v1329 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v1328);
                                *(_QWORD *)(v1329 + 8 * v1296) = v1287;
                                v1330 = (char *)v1315[40];
                                sub_141758A00(a1: v1329, a2: v1315[39], a3: &v1314[-v1315[39]]);
                                if ( v1330 != v1314 )
                                  sub_141758A00(a1: v1329 + 8 * v1296 + 8, a2: v1314, a3: v1315[40] - (_QWORD)v1314);
                                v1331 = v1315[39];
                                v1215 = v1604;
                                if ( v1331 != 0 )
                                {
                                  v1332 = v1315;
                                  v1333 = v1315[41] - v1331;
                                  if ( v1333 == -1 )
                                    v1333 = *(unsigned int *)(v1331 - *(unsigned int *)(qword_141ABD470 + 48));
                                  if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                                    && (v1334 = *(_QWORD *)(qword_141ABD470 + 24),
                                        (*(_QWORD *)(qword_141ABD470 + 32) - v1334) >> 3 > v1333)
                                    && (v1335 = *(_QWORD *)(v1334 + 8 * v1333)) != 0 )
                                  {
                                    MEMORY[0x1419475D8](a1: v1335 + 32, a2: v1331 - *(unsigned int *)(v1335 + 120));
                                    v1336 = *(_BYTE *)(v1335 + 72) != 0
                                         && _InterlockedDecrement((volatile signed __int32 *)(v1335 + 64)) != 0;
                                    v1315 = v1332;
                                    if ( !v1336 && *(_BYTE *)(v1335 + 97) != 0 )
                                      sub_1412D33C0(a1: v1335);
                                  }
                                  else
                                  {
                                    MEMORY[0x141948990](a1: v1331 - *(unsigned int *)(qword_141ABD470 + 48));
                                    v1315 = v1332;
                                  }
                                }
                                v1315[39] = v1329;
                                v1315[40] = v1329 + 8 * v1597;
                                v1315[41] = v1329 + 8 * v1328;
                                v32 = (__int64)v1315;
                                goto LABEL_2542;
                              }
                              if ( v1291 != (_QWORD *)v1314 )
                              {
                                *v1291 = *(v1291 - 1);
                                v32 = (__int64)v1603;
                                v1603[40] += 8LL;
                                sub_141758A00(a1: v1314 + 8, a2: v1314, a3: (char *)(v1291 - 1) - v1314);
                                *(_QWORD *)v1314 = v1287;
                                goto LABEL_2541;
                              }
                              *v1291 = v1287;
                              v32 = (__int64)v1603;
                            }
                            break;
                          }
                          *(_QWORD *)(v32 + 320) += 8LL;
                          goto LABEL_2541;
                        }
LABEL_2928:
                        v1469 = qword_141B59FA0;
                        if ( qword_141B59FA0 != 0 && v1581 != 0 )
                        {
                          v1470 = v1580;
                          v1471 = (unsigned int)MEMORY[0x141947498]();
                          v1472 = *(_QWORD *)(v1469 + 16);
                          if ( v1472 == 0 || v1472 == (unsigned int)v1471 )
                          {
                            if ( v1470 == 0 )
                              v1471 = 0;
                            *(_QWORD *)(v1469 + 16) = v1471;
                          }
                          *(_QWORD *)(v1469 + 8) = v1579;
                        }
LABEL_2936:
                        LODWORD(v32) = 0;
                        return (unsigned int)v32;
                      }
                      v949 = (int)v1602;
                      v950 = v424;
                      if ( v424 )
                      {
                        v646 = *(_QWORD *)(v10 + 120);
                        v951 = (*(_QWORD *)(v10 + 128) - v646) >> 3;
                        v952 = v951 + (int)v1602;
                        v953 = (*(_QWORD *)(v10 + 136) - v646) >> 3;
                        LOBYTE(v10) = v1604;
                        if ( v953 >= v952 )
                          goto LABEL_2224;
                        if ( v952 >> 61 == 0 )
                        {
                          v32 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v952);
                          sub_141758A00(a1: v32, a2: a1[15], a3: a1[16] - a1[15]);
                          if ( a1[15] != 0 )
                            sub_1407E4890(a1: qword_141ABD470);
                          a1[15] = v32;
                          a1[16] = v32 + 8 * v951;
                          v646 = v32 + 8 * v952;
                          a1[17] = v646;
                          goto LABEL_2224;
                        }
LABEL_3122:
                        sub_1400526C0(a1: v953);
                      }
                      v32 = *(_QWORD *)(v10 + 120);
                      v953 = (*(_QWORD *)(v10 + 136) - v32) >> 3;
                      LOBYTE(v10) = v1604;
                      if ( v953 < (int)v1602 )
                      {
                        if ( (int)v1602 < 0 )
                          goto LABEL_3122;
                        v1138 = a1[16];
                        v1139 = a1;
                        v1140 = sub_1407E4490(a1: qword_141ABD470, a2: 8LL * (int)v1602);
                        sub_141758A00(a1: v1140, a2: v1139[15], a3: v1139[16] - v1139[15]);
                        if ( v1139[15] != 0 )
                          sub_1407E4890(a1: qword_141ABD470);
                        v1139[15] = v1140;
                        v1139[16] = v1140 + v1138 - v32;
                        v646 = v1140 + 8 * v949;
                        v1139[17] = v646;
                        a1 = v1139;
                      }
LABEL_2224:
                      if ( (int)v1602 <= 0 )
                      {
                        LOBYTE(v646) = 1;
                        LODWORD(v1599) = v646;
                        goto LABEL_731;
                      }
                      v1141 = 0;
                      if ( !v950 )
                      {
                        v1218 = v1597;
                        do
                        {
                          if ( dword_141B60A20 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer
                                                             + (unsigned int)TlsIndex)
                                                           + 4LL) )
                          {
                            sub_141750E08(a1: &dword_141B60A20);
                            if ( dword_141B60A20 == -1 )
                            {
                              sub_1407E53D0(
                                a1: (unsigned int)&unk_141B609D0,
                                a2: 1100150576,
                                a3: 128,
                                a4: 32,
                                a5: 0,
                                a6: 1,
                                a7: 128,
                                a8: 4096);
                              sub_141751048(a1: sub_140FE1B20);
                              sub_141750EA0(a1: &dword_141B60A20);
                            }
                          }
                          v1219 = sub_1407E58C0(a1: &unk_141B609D0, a2: 32);
                          *(_QWORD *)v1219 = 0;
                          *(_QWORD *)(v1219 + 8) = 0;
                          *(_QWORD *)(v1219 + 16) = 0;
                          *(_WORD *)(v1219 + 28) = -1;
                          *(_DWORD *)(v1219 + 24) = 0;
                          v1587[0] = v1595;
                          if ( v1595 != nullptr )
                            _InterlockedIncrement(v1595 + 2);
                          v1220 = sub_140E498B0(a1: v1219, a2: v1587, a3: v1218);
                          v1221 = (void (__fastcall ***)(_QWORD, __int64))v1587[0];
                          if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] + 8LL)) == 0 )
                            (**v1221)(a1: v1221, a2: 1);
                          LODWORD(v1599) = v1220;
                          if ( (_BYTE)v1220 == 0 )
                            break;
                          v32 = a1[16];
                          if ( v32 == a1[17] )
                          {
                            v1222 = v32 - a1[15];
                            v1223 = v1222 >> 3;
                            v10 = (__int64)a1;
                            v1224 = (unsigned __int64)(v1222 >> 3) >> 1;
                            v1225 = 0x1FFFFFFFFFFFFFFFLL - v1224;
                            v1226 = (v1222 >> 3) + v1224;
                            v1598 = (v1222 >> 3) + 1;
                            if ( v1226 <= v1598 )
                              v1226 = v1223 + 1;
                            if ( v1223 > v1225 )
                              v1226 = 0x1FFFFFFFFFFFFFFFLL;
                            v1227 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v1226);
                            *(_QWORD *)(v1227 + v1222) = v1219;
                            v1228 = *(_QWORD *)(v10 + 128);
                            sub_141758A00(a1: v1227, a2: *(_QWORD *)(v10 + 120), a3: v32 - *(_QWORD *)(v10 + 120));
                            if ( v1228 != v32 )
                              sub_141758A00(a1: v1227 + v1222 + 8, a2: v32, a3: *(_QWORD *)(v10 + 128) - v32);
                            v1229 = *(_QWORD *)(v10 + 120);
                            v1218 = v1597;
                            if ( v1229 != 0 )
                            {
                              v1230 = *(_QWORD *)(v10 + 136) - v1229;
                              if ( v1230 == -1 )
                                v1230 = *(unsigned int *)(v1229 - *(unsigned int *)(qword_141ABD470 + 48));
                              if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                                && (v1231 = *(_QWORD *)(qword_141ABD470 + 24),
                                    (*(_QWORD *)(qword_141ABD470 + 32) - v1231) >> 3 > v1230)
                                && (v32 = *(_QWORD *)(v1231 + 8 * v1230)) != 0 )
                              {
                                MEMORY[0x1419475D8](a1: v32 + 32, a2: v1229 - *(unsigned int *)(v32 + 120));
                                v1232 = *(_BYTE *)(v32 + 72) != 0
                                     && _InterlockedDecrement((volatile signed __int32 *)(v32 + 64)) != 0;
                                v10 = (__int64)v1603;
                                if ( !v1232 && *(_BYTE *)(v32 + 97) != 0 )
                                  sub_1412D33C0(a1: v32);
                              }
                              else
                              {
                                MEMORY[0x141948990](a1: v1229 - *(unsigned int *)(qword_141ABD470 + 48));
                                v10 = (__int64)v1603;
                              }
                            }
                            *(_QWORD *)(v10 + 120) = v1227;
                            *(_QWORD *)(v10 + 128) = v1227 + 8 * v1598;
                            *(_QWORD *)(v10 + 136) = v1227 + 8 * v1226;
                            a1 = (_QWORD *)v10;
                            LOBYTE(v10) = v1604;
                          }
                          else
                          {
                            *(_QWORD *)v32 = v1219;
                            a1[16] += 8LL;
                          }
                          ++v1141;
                        }
                        while ( v1141 < (int)v1602 );
                        goto LABEL_731;
                      }
                      v1142 = v1597;
                      while ( 2 )
                      {
                        if ( dword_141B60A20 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer
                                                           + (unsigned int)TlsIndex)
                                                         + 4LL) )
                        {
                          sub_141750E08(a1: &dword_141B60A20);
                          if ( dword_141B60A20 == -1 )
                          {
                            sub_1407E53D0(
                              a1: (unsigned int)&unk_141B609D0,
                              a2: 1100150576,
                              a3: 128,
                              a4: 32,
                              a5: 0,
                              a6: 1,
                              a7: 128,
                              a8: 4096);
                            sub_141751048(a1: sub_140FE1B20);
                            sub_141750EA0(a1: &dword_141B60A20);
                          }
                        }
                        v32 = sub_1407E58C0(a1: &unk_141B609D0, a2: 32);
                        *(_QWORD *)v32 = 0;
                        *(_QWORD *)(v32 + 8) = 0;
                        *(_QWORD *)(v32 + 16) = 0;
                        *(_WORD *)(v32 + 28) = -1;
                        *(_DWORD *)(v32 + 24) = 0;
                        v1587[0] = v1595;
                        if ( v1595 != nullptr )
                          _InterlockedIncrement(v1595 + 2);
                        v1163 = sub_140E498B0(a1: v32, a2: v1587, a3: v1142);
                        v1164 = (void (__fastcall ***)(_QWORD, __int64))v1587[0];
                        if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] + 8LL)) == 0 )
                          (**v1164)(a1: v1164, a2: 1);
                        if ( (_BYTE)v1163 == 0 )
                        {
                          LODWORD(v1599) = 0;
                          goto LABEL_731;
                        }
                        LODWORD(v1598) = v1141;
                        LODWORD(v1599) = v1163;
                        v1165 = a1[15];
                        v1166 = (__int64)a1;
                        v1167 = (__int64 *)a1[16];
                        v1168 = (__int64)v1167 - v1165;
                        v1169 = (__int64 *)v1165;
                        if ( (__int64)v1167 - v1165 > 0 )
                        {
                          v1170 = (unsigned __int64)v1168 >> 3;
                          v1169 = (__int64 *)v1165;
                          v1171 = (unsigned __int64)v1168 >> 3;
                          do
                          {
                            v1171 = (unsigned __int64)v1171 >> 1;
                            if ( *(_DWORD *)(v1169[v1171] + 24) < *(_DWORD *)(v32 + 24) )
                            {
                              v1169 += v1171 + 1;
                              v1171 = v1170 + ~v1171;
                            }
                            v1170 = v1171;
                          }
                          while ( v1171 > 0 );
                        }
                        if ( v1169 == v1167 )
                        {
                          if ( v1167 != *(__int64 **)(v1166 + 136) )
                          {
                            *v1167 = v32;
                            *(_QWORD *)(v1166 + 128) += 8LL;
                            a1 = (_QWORD *)v1166;
                            goto LABEL_2274;
                          }
                          v10 = v1166;
                          v1191 = (unsigned __int64)(v1168 >> 3) >> 1;
                          v1192 = 0x1FFFFFFFFFFFFFFFLL - v1191;
                          v1193 = (v1168 >> 3) + v1191;
                          if ( v1193 <= (v1168 >> 3) + 1 )
                            v1193 = (v1168 >> 3) + 1;
                          if ( v1168 >> 3 > v1192 )
                            v1193 = 0x1FFFFFFFFFFFFFFFLL;
                          v1194 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v1193);
                          *(_QWORD *)(v1194 + v1168) = v32;
                          v1195 = *(__int64 **)(v10 + 128);
                          sub_141758A00(
                            a1: v1194,
                            a2: *(_QWORD *)(v10 + 120),
                            a3: (char *)v1167 - *(_QWORD *)(v10 + 120));
                          if ( v1195 != v1167 )
                            sub_141758A00(a1: v1194 + v1168 + 8, a2: v1167, a3: *(_QWORD *)(v10 + 128) - (_QWORD)v1167);
                          v1196 = v1194;
                          v1197 = *(_QWORD *)(v10 + 120);
                          v1142 = v1597;
                          if ( v1197 != 0 )
                          {
                            v1198 = *(_QWORD *)(v10 + 136) - v1197;
                            if ( v1198 == -1 )
                              v1198 = *(unsigned int *)(v1197 - *(unsigned int *)(qword_141ABD470 + 48));
                            if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                              && (v1199 = *(_QWORD *)(qword_141ABD470 + 24),
                                  (*(_QWORD *)(qword_141ABD470 + 32) - v1199) >> 3 > v1198)
                              && (v32 = *(_QWORD *)(v1199 + 8 * v1198)) != 0 )
                            {
                              MEMORY[0x1419475D8](a1: v32 + 32, a2: v1197 - *(unsigned int *)(v32 + 120));
                              v1200 = *(_BYTE *)(v32 + 72) != 0
                                   && _InterlockedDecrement((volatile signed __int32 *)(v32 + 64)) != 0;
                              v10 = (__int64)v1603;
                              if ( !v1200 && *(_BYTE *)(v32 + 97) != 0 )
                                sub_1412D33C0(a1: v32);
                            }
                            else
                            {
                              MEMORY[0x141948990](a1: v1197 - *(unsigned int *)(qword_141ABD470 + 48));
                              v10 = (__int64)v1603;
                            }
                          }
                          *(_QWORD *)(v10 + 120) = v1196;
                          *(_QWORD *)(v10 + 128) = v1196 + 8 * ((v1168 >> 3) + 1);
                          *(_QWORD *)(v10 + 136) = v1196 + 8 * v1193;
                          a1 = (_QWORD *)v10;
                          LOBYTE(v10) = v1604;
                        }
                        else
                        {
                          v1172 = ((__int64)v1169 - v1165) >> 3;
                          if ( *(_DWORD *)(*v1169 + 24) == *(_DWORD *)(v32 + 24) )
                          {
                            v1173 = v1168 >> 3;
                            if ( v1173 > v1172 )
                            {
                              v1174 = *(__int64 **)(v1165 + 8 * v1172);
                              if ( v1174 != nullptr )
                              {
                                sub_140E44A40(a1: v1174 + 2);
                                v1175 = v1174[1];
                                if ( v1175 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1175 - 4)) == 0 )
                                  sub_1412EC9A0(a1: v1175 - 4);
                                v1176 = *v1174;
                                if ( *v1174 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1176 - 4)) == 0 )
                                  sub_1412EC9A0(a1: v1176 - 4);
                                sub_140FE19C0(a1: v1174);
                                v1165 = v1603[15];
                                v1167 = (__int64 *)v1603[16];
                                v1173 = ((__int64)v1167 - v1165) >> 3;
                              }
                            }
                            if ( v1173 <= v1172 )
                            {
                              v1177 = v1172 + 1;
                              v1178 = v1172 + 1 - v1173;
                              if ( v1172 + 1 < v1173 )
                              {
                                v1603[16] = v1165 + 8 * v1177;
                              }
                              else if ( v1172 + 1 > v1173 )
                              {
                                v1179 = v1603;
                                v1180 = (v1603[17] - v1165) >> 3;
                                if ( v1180 >= v1177 )
                                {
                                  v1211 = &v1167[v1178];
                                  sub_141758A10(a1: v1167, a2: 0, a3: 8 * v1178);
                                  v1179[16] = v1211;
                                  v1165 = v1179[15];
                                }
                                else
                                {
                                  v953 = v1177 >> 61;
                                  if ( v1177 >> 61 != 0 )
                                    goto LABEL_3122;
                                  v1181 = v1180 + (v1180 >> 1);
                                  if ( v1181 <= v1177 )
                                    v1181 = v1172 + 1;
                                  if ( v1180 > 0x1FFFFFFFFFFFFFFFLL - (v1180 >> 1) )
                                    v1181 = 0x1FFFFFFFFFFFFFFFLL;
                                  v1165 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v1181);
                                  sub_141758A10(a1: v1165 + 8 * v1173, a2: 0, a3: 8 * (v1172 + 1 - v1173));
                                  v1182 = v1603;
                                  sub_141758A00(a1: v1165, a2: v1603[15], a3: v1603[16] - v1603[15]);
                                  v1183 = v1182[15];
                                  if ( v1183 != 0 )
                                  {
                                    v1184 = v1182[17] - v1183;
                                    if ( v1184 == -1 )
                                      v1184 = *(unsigned int *)(v1183 - *(unsigned int *)(qword_141ABD470 + 48));
                                    if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                                      && (v1185 = *(_QWORD *)(qword_141ABD470 + 24),
                                          (*(_QWORD *)(qword_141ABD470 + 32) - v1185) >> 3 > v1184)
                                      && (v1186 = *(_QWORD *)(v1185 + 8 * v1184)) != 0 )
                                    {
                                      MEMORY[0x1419475D8](a1: v1186 + 32, a2: v1183 - *(unsigned int *)(v1186 + 120));
                                      v1187 = *(_BYTE *)(v1186 + 72) != 0
                                           && _InterlockedDecrement((volatile signed __int32 *)(v1186 + 64)) != 0;
                                      v1182 = v1603;
                                      if ( !v1187 && *(_BYTE *)(v1186 + 97) != 0 )
                                        sub_1412D33C0(a1: v1186);
                                    }
                                    else
                                    {
                                      MEMORY[0x141948990](a1: v1183 - *(unsigned int *)(qword_141ABD470 + 48));
                                      v1182 = v1603;
                                    }
                                  }
                                  v1182[15] = v1165;
                                  v1182[16] = v1165 + 8 * (v1172 + 1);
                                  v1182[17] = v1165 + 8 * v1181;
                                }
                                LOBYTE(v10) = v1604;
                              }
                            }
                            *(_QWORD *)(v1165 + 8 * v1172) = v32;
                            a1 = v1603;
                          }
                          else
                          {
                            v1188 = (__int64 *)(v1165 + 8 * v1172);
                            v10 = (__int64)v1603;
                            if ( v1167 == (__int64 *)v1603[17] )
                            {
                              v1201 = v1168 >> 3;
                              v1202 = v1201 + 1;
                              v1203 = v1201 + (v1201 >> 1);
                              if ( v1203 <= v1201 + 1 )
                                v1203 = v1201 + 1;
                              if ( v1201 > 0x1FFFFFFFFFFFFFFFLL - (v1201 >> 1) )
                                v1203 = 0x1FFFFFFFFFFFFFFFLL;
                              v1204 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v1203);
                              *(_QWORD *)(v1204 + 8 * v1172) = v32;
                              v1205 = *(__int64 **)(v10 + 128);
                              sub_141758A00(
                                a1: v1204,
                                a2: *(_QWORD *)(v10 + 120),
                                a3: (char *)v1188 - *(_QWORD *)(v10 + 120));
                              if ( v1205 != v1188 )
                                sub_141758A00(
                                  a1: v1204 + 8 * v1172 + 8,
                                  a2: v1188,
                                  a3: *(_QWORD *)(v10 + 128) - (_QWORD)v1188);
                              v1206 = *(_QWORD *)(v10 + 120);
                              LODWORD(v32) = (unsigned __int8)v1604;
                              if ( v1206 != 0 )
                              {
                                v1207 = *(_QWORD *)(v10 + 136) - v1206;
                                if ( v1207 == -1 )
                                  v1207 = *(unsigned int *)(v1206 - *(unsigned int *)(qword_141ABD470 + 48));
                                if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                                  && (v1208 = *(_QWORD *)(qword_141ABD470 + 24),
                                      (*(_QWORD *)(qword_141ABD470 + 32) - v1208) >> 3 > v1207)
                                  && (v1209 = *(_QWORD *)(v1208 + 8 * v1207)) != 0 )
                                {
                                  MEMORY[0x1419475D8](a1: v1209 + 32, a2: v1206 - *(unsigned int *)(v1209 + 120));
                                  v1210 = *(_BYTE *)(v1209 + 72) != 0
                                       && _InterlockedDecrement((volatile signed __int32 *)(v1209 + 64)) != 0;
                                  v10 = (__int64)v1603;
                                  if ( !v1210 && *(_BYTE *)(v1209 + 97) != 0 )
                                    sub_1412D33C0(a1: v1209);
                                }
                                else
                                {
                                  MEMORY[0x141948990](a1: v1206 - *(unsigned int *)(qword_141ABD470 + 48));
                                  v10 = (__int64)v1603;
                                }
                              }
                              *(_QWORD *)(v10 + 120) = v1204;
                              *(_QWORD *)(v10 + 128) = v1204 + 8 * v1202;
                              *(_QWORD *)(v10 + 136) = v1204 + 8 * v1203;
                              a1 = (_QWORD *)v10;
                              LOBYTE(v10) = v32;
                            }
                            else
                            {
                              if ( v1167 == v1188 )
                              {
                                *v1167 = v32;
                                a1 = v1603;
                                v1603[16] += 8LL;
                              }
                              else
                              {
                                *v1167 = *(v1167 - 1);
                                v1189 = v1603;
                                v1603[16] += 8LL;
                                v1190 = (char *)(v1167 - 1) - (char *)v1188;
                                a1 = v1189;
                                sub_141758A00(a1: v1188 + 1, a2: v1165 + 8 * v1172, a3: v1190);
                                *v1188 = v32;
                              }
                              LOBYTE(v10) = v1604;
                            }
                          }
LABEL_2274:
                          v1142 = v1597;
                        }
                        v1141 = v1598 + 1;
                        if ( (int)v1598 + 1 >= (int)v1602 )
                          goto LABEL_731;
                        continue;
                      }
                    }
                    v748 = (int)v1602;
                    v749 = v306;
                    if ( v306 )
                    {
                      v439 = *(_QWORD *)(v10 + 288);
                      v750 = (*(_QWORD *)(v10 + 296) - v439) >> 3;
                      v751 = v750 + (int)v1602;
                      v752 = (*(_QWORD *)(v10 + 304) - v439) >> 3;
                      LOBYTE(v10) = v1604;
                      if ( v752 >= v751 )
                        goto LABEL_1908;
                      if ( v751 >> 61 == 0 )
                      {
                        v32 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v751);
                        sub_141758A00(a1: v32, a2: a1[36], a3: a1[37] - a1[36]);
                        if ( a1[36] != 0 )
                          sub_1407E4890(a1: qword_141ABD470);
                        a1[36] = v32;
                        a1[37] = v32 + 8 * v750;
                        v439 = v32 + 8 * v751;
                        a1[38] = v439;
                        goto LABEL_1908;
                      }
LABEL_3121:
                      sub_1400526C0(a1: v752);
                    }
                    v32 = *(_QWORD *)(v10 + 288);
                    v752 = (*(_QWORD *)(v10 + 304) - v32) >> 3;
                    LOBYTE(v10) = v1604;
                    if ( v752 < (int)v1602 )
                    {
                      if ( (int)v1602 < 0 )
                        goto LABEL_3121;
                      v982 = a1[37];
                      v983 = a1;
                      v984 = sub_1407E4490(a1: qword_141ABD470, a2: 8LL * (int)v1602);
                      sub_141758A00(a1: v984, a2: v983[36], a3: v983[37] - v983[36]);
                      if ( v983[36] != 0 )
                        sub_1407E4890(a1: qword_141ABD470);
                      v983[36] = v984;
                      v983[37] = v984 + v982 - v32;
                      v439 = v984 + 8 * v748;
                      v983[38] = v439;
                      a1 = v983;
                    }
LABEL_1908:
                    if ( (int)v1602 <= 0 )
                    {
                      LOBYTE(v439) = 1;
                      LODWORD(v1599) = v439;
                      goto LABEL_499;
                    }
                    v985 = 0;
                    if ( !v749 )
                    {
                      v1143 = v1597;
                      do
                      {
                        if ( dword_141B60868 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer
                                                           + (unsigned int)TlsIndex)
                                                         + 4LL) )
                        {
                          sub_141750E08(a1: &dword_141B60868);
                          if ( dword_141B60868 == -1 )
                          {
                            sub_1407E53D0(
                              a1: (unsigned int)&unk_141B60818,
                              a2: 1100150664,
                              a3: 512,
                              a4: 16,
                              a5: 0,
                              a6: 1,
                              a7: 512,
                              a8: 4096);
                            sub_141751048(a1: sub_140FE13F0);
                            sub_141750EA0(a1: &dword_141B60868);
                          }
                        }
                        v1144 = sub_1407E58C0(a1: &unk_141B60818, a2: 16);
                        *(_WORD *)(v1144 + 4) = -1;
                        *(_QWORD *)(v1144 + 8) = 0;
                        *(_DWORD *)v1144 = 0;
                        v1587[0] = v1595;
                        if ( v1595 != nullptr )
                          _InterlockedIncrement(v1595 + 2);
                        v1145 = sub_14159B8E0(a1: v1144, a2: v1587, a3: v1143);
                        v1146 = (void (__fastcall ***)(_QWORD, __int64))v1587[0];
                        if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] + 8LL)) == 0 )
                          (**v1146)(a1: v1146, a2: 1);
                        LODWORD(v1599) = v1145;
                        if ( (_BYTE)v1145 == 0 )
                          break;
                        v32 = a1[37];
                        if ( v32 == a1[38] )
                        {
                          v1147 = v32 - a1[36];
                          v1148 = v1147 >> 3;
                          v10 = (__int64)a1;
                          v1149 = (unsigned __int64)(v1147 >> 3) >> 1;
                          v1150 = 0x1FFFFFFFFFFFFFFFLL - v1149;
                          v1151 = (v1147 >> 3) + v1149;
                          v1598 = (v1147 >> 3) + 1;
                          if ( v1151 <= v1598 )
                            v1151 = v1148 + 1;
                          if ( v1148 > v1150 )
                            v1151 = 0x1FFFFFFFFFFFFFFFLL;
                          v1152 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v1151);
                          *(_QWORD *)(v1152 + v1147) = v1144;
                          v1153 = *(_QWORD *)(v10 + 296);
                          sub_141758A00(a1: v1152, a2: *(_QWORD *)(v10 + 288), a3: v32 - *(_QWORD *)(v10 + 288));
                          if ( v1153 != v32 )
                            sub_141758A00(a1: v1152 + v1147 + 8, a2: v32, a3: *(_QWORD *)(v10 + 296) - v32);
                          v1154 = *(_QWORD *)(v10 + 288);
                          v1143 = v1597;
                          if ( v1154 != 0 )
                          {
                            v1155 = *(_QWORD *)(v10 + 304) - v1154;
                            if ( v1155 == -1 )
                              v1155 = *(unsigned int *)(v1154 - *(unsigned int *)(qword_141ABD470 + 48));
                            if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                              && (v1156 = *(_QWORD *)(qword_141ABD470 + 24),
                                  (*(_QWORD *)(qword_141ABD470 + 32) - v1156) >> 3 > v1155)
                              && (v32 = *(_QWORD *)(v1156 + 8 * v1155)) != 0 )
                            {
                              MEMORY[0x1419475D8](a1: v32 + 32, a2: v1154 - *(unsigned int *)(v32 + 120));
                              v1157 = *(_BYTE *)(v32 + 72) != 0
                                   && _InterlockedDecrement((volatile signed __int32 *)(v32 + 64)) != 0;
                              v10 = (__int64)v1603;
                              if ( !v1157 && *(_BYTE *)(v32 + 97) != 0 )
                                sub_1412D33C0(a1: v32);
                            }
                            else
                            {
                              MEMORY[0x141948990](a1: v1154 - *(unsigned int *)(qword_141ABD470 + 48));
                              v10 = (__int64)v1603;
                            }
                          }
                          *(_QWORD *)(v10 + 288) = v1152;
                          *(_QWORD *)(v10 + 296) = v1152 + 8 * v1598;
                          *(_QWORD *)(v10 + 304) = v1152 + 8 * v1151;
                          a1 = (_QWORD *)v10;
                          LOBYTE(v10) = v1604;
                        }
                        else
                        {
                          *(_QWORD *)v32 = v1144;
                          a1[37] += 8LL;
                        }
                        ++v985;
                      }
                      while ( v985 < (int)v1602 );
                      goto LABEL_499;
                    }
                    v986 = v1597;
                    while ( 2 )
                    {
                      if ( dword_141B60868 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer
                                                         + (unsigned int)TlsIndex)
                                                       + 4LL) )
                      {
                        sub_141750E08(a1: &dword_141B60868);
                        if ( dword_141B60868 == -1 )
                        {
                          sub_1407E53D0(
                            a1: (unsigned int)&unk_141B60818,
                            a2: 1100150664,
                            a3: 512,
                            a4: 16,
                            a5: 0,
                            a6: 1,
                            a7: 512,
                            a8: 4096);
                          sub_141751048(a1: sub_140FE13F0);
                          sub_141750EA0(a1: &dword_141B60868);
                        }
                      }
                      v32 = sub_1407E58C0(a1: &unk_141B60818, a2: 16);
                      *(_WORD *)(v32 + 4) = -1;
                      *(_QWORD *)(v32 + 8) = 0;
                      *(_DWORD *)v32 = 0;
                      v1587[0] = v1595;
                      if ( v1595 != nullptr )
                        _InterlockedIncrement(v1595 + 2);
                      v1085 = sub_14159B8E0(a1: v32, a2: v1587, a3: v986);
                      v1086 = (void (__fastcall ***)(_QWORD, __int64))v1587[0];
                      if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] + 8LL)) == 0 )
                        (**v1086)(a1: v1086, a2: 1);
                      if ( (_BYTE)v1085 == 0 )
                      {
                        LODWORD(v1599) = 0;
                        goto LABEL_499;
                      }
                      LODWORD(v1598) = v985;
                      LODWORD(v1599) = v1085;
                      v1087 = a1[36];
                      v1088 = (__int64)a1;
                      v1089 = (__int64 *)a1[37];
                      v1090 = (__int64)v1089 - v1087;
                      v1091 = (__int64 *)v1087;
                      if ( (__int64)v1089 - v1087 > 0 )
                      {
                        v1092 = (unsigned __int64)v1090 >> 3;
                        v1091 = (__int64 *)v1087;
                        v1093 = (unsigned __int64)v1090 >> 3;
                        do
                        {
                          v1093 = (unsigned __int64)v1093 >> 1;
                          if ( *(_DWORD *)v1091[v1093] < *(_DWORD *)v32 )
                          {
                            v1091 += v1093 + 1;
                            v1093 = v1092 + ~v1093;
                          }
                          v1092 = v1093;
                        }
                        while ( v1093 > 0 );
                      }
                      if ( v1091 == v1089 )
                      {
                        if ( v1089 != *(__int64 **)(v1088 + 304) )
                        {
                          *v1089 = v32;
                          *(_QWORD *)(v1088 + 296) += 8LL;
                          a1 = (_QWORD *)v1088;
                          goto LABEL_2120;
                        }
                        v10 = v1088;
                        v1111 = (unsigned __int64)(v1090 >> 3) >> 1;
                        v1112 = 0x1FFFFFFFFFFFFFFFLL - v1111;
                        v1113 = (v1090 >> 3) + v1111;
                        if ( v1113 <= (v1090 >> 3) + 1 )
                          v1113 = (v1090 >> 3) + 1;
                        if ( v1090 >> 3 > v1112 )
                          v1113 = 0x1FFFFFFFFFFFFFFFLL;
                        v1114 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v1113);
                        *(_QWORD *)(v1114 + v1090) = v32;
                        v1115 = *(__int64 **)(v10 + 296);
                        sub_141758A00(a1: v1114, a2: *(_QWORD *)(v10 + 288), a3: (char *)v1089 - *(_QWORD *)(v10 + 288));
                        if ( v1115 != v1089 )
                          sub_141758A00(a1: v1114 + v1090 + 8, a2: v1089, a3: *(_QWORD *)(v10 + 296) - (_QWORD)v1089);
                        v1116 = v1114;
                        v1117 = *(_QWORD *)(v10 + 288);
                        v986 = v1597;
                        v1084 = v1598;
                        if ( v1117 != 0 )
                        {
                          v1118 = *(_QWORD *)(v10 + 304) - v1117;
                          if ( v1118 == -1 )
                            v1118 = *(unsigned int *)(v1117 - *(unsigned int *)(qword_141ABD470 + 48));
                          if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                            && (v1119 = *(_QWORD *)(qword_141ABD470 + 24),
                                (*(_QWORD *)(qword_141ABD470 + 32) - v1119) >> 3 > v1118)
                            && (v32 = *(_QWORD *)(v1119 + 8 * v1118)) != 0 )
                          {
                            MEMORY[0x1419475D8](a1: v32 + 32, a2: v1117 - *(unsigned int *)(v32 + 120));
                            v1120 = *(_BYTE *)(v32 + 72) != 0
                                 && _InterlockedDecrement((volatile signed __int32 *)(v32 + 64)) != 0;
                            v10 = (__int64)v1603;
                            if ( !v1120 && *(_BYTE *)(v32 + 97) != 0 )
                              sub_1412D33C0(a1: v32);
                          }
                          else
                          {
                            MEMORY[0x141948990](a1: v1117 - *(unsigned int *)(qword_141ABD470 + 48));
                            v10 = (__int64)v1603;
                          }
                        }
                        *(_QWORD *)(v10 + 288) = v1116;
                        *(_QWORD *)(v10 + 296) = v1116 + 8 * ((v1090 >> 3) + 1);
                        *(_QWORD *)(v10 + 304) = v1116 + 8 * v1113;
                        a1 = (_QWORD *)v10;
                        LOBYTE(v10) = v1604;
                      }
                      else
                      {
                        v1094 = ((__int64)v1091 - v1087) >> 3;
                        if ( *(_DWORD *)*v1091 == *(_DWORD *)v32 )
                        {
                          v1095 = v1090 >> 3;
                          if ( v1095 > v1094 )
                          {
                            v1096 = *(_QWORD *)(v1087 + 8 * v1094);
                            if ( v1096 != 0 )
                            {
                              sub_140E44A40(a1: v1096 + 8);
                              sub_140FE1290(a1: v1096);
                              v1087 = v1603[36];
                              v1089 = (__int64 *)v1603[37];
                              v1095 = ((__int64)v1089 - v1087) >> 3;
                            }
                          }
                          if ( v1095 <= v1094 )
                          {
                            v1097 = v1094 + 1;
                            v1098 = v1094 + 1 - v1095;
                            if ( v1094 + 1 < v1095 )
                            {
                              v1603[37] = v1087 + 8 * v1097;
                            }
                            else if ( v1094 + 1 > v1095 )
                            {
                              v1099 = (v1603[38] - v1087) >> 3;
                              if ( v1099 >= v1097 )
                              {
                                v1129 = v1603;
                                sub_141758A10(a1: v1089, a2: 0, a3: 8 * v1098);
                                v1129[37] = &v1089[v1098];
                                v1087 = v1129[36];
                              }
                              else
                              {
                                v752 = v1097 >> 61;
                                if ( v1097 >> 61 != 0 )
                                  goto LABEL_3121;
                                v1100 = v1099 + (v1099 >> 1);
                                if ( v1100 <= v1097 )
                                  v1100 = v1094 + 1;
                                if ( v1099 > 0x1FFFFFFFFFFFFFFFLL - (v1099 >> 1) )
                                  v1100 = 0x1FFFFFFFFFFFFFFFLL;
                                v1087 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v1100);
                                sub_141758A10(a1: v1087 + 8 * v1095, a2: 0, a3: 8 * v1098);
                                v1101 = v1603;
                                sub_141758A00(a1: v1087, a2: v1603[36], a3: v1603[37] - v1603[36]);
                                v1102 = v1101[36];
                                if ( v1102 != 0 )
                                {
                                  v1103 = v1101[38] - v1102;
                                  if ( v1103 == -1 )
                                    v1103 = *(unsigned int *)(v1102 - *(unsigned int *)(qword_141ABD470 + 48));
                                  if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                                    && (v1104 = *(_QWORD *)(qword_141ABD470 + 24),
                                        (*(_QWORD *)(qword_141ABD470 + 32) - v1104) >> 3 > v1103)
                                    && (v1105 = *(_QWORD *)(v1104 + 8 * v1103)) != 0 )
                                  {
                                    MEMORY[0x1419475D8](a1: v1105 + 32, a2: v1102 - *(unsigned int *)(v1105 + 120));
                                    v1106 = *(_BYTE *)(v1105 + 72) != 0
                                         && _InterlockedDecrement((volatile signed __int32 *)(v1105 + 64)) != 0;
                                    v1101 = v1603;
                                    if ( !v1106 && *(_BYTE *)(v1105 + 97) != 0 )
                                      sub_1412D33C0(a1: v1105);
                                  }
                                  else
                                  {
                                    MEMORY[0x141948990](a1: v1102 - *(unsigned int *)(qword_141ABD470 + 48));
                                    v1101 = v1603;
                                  }
                                }
                                v1101[36] = v1087;
                                v1101[37] = v1087 + 8 * (v1094 + 1);
                                v1101[38] = v1087 + 8 * v1100;
                              }
                            }
                          }
                          *(_QWORD *)(v1087 + 8 * v1094) = v32;
                          a1 = v1603;
LABEL_2119:
                          LOBYTE(v10) = v1604;
                        }
                        else
                        {
                          v1107 = (__int64 *)(v1087 + 8 * v1094);
                          v1108 = v1603;
                          if ( v1089 != (__int64 *)v1603[38] )
                          {
                            if ( v1089 == v1107 )
                            {
                              *v1089 = v32;
                              a1 = v1603;
                              v1603[37] += 8LL;
                            }
                            else
                            {
                              *v1089 = *(v1089 - 1);
                              v1109 = v1603;
                              v1603[37] += 8LL;
                              v1110 = (char *)(v1089 - 1) - (char *)v1107;
                              a1 = v1109;
                              sub_141758A00(a1: v1107 + 1, a2: v1087 + 8 * v1094, a3: v1110);
                              *v1107 = v32;
                            }
                            goto LABEL_2119;
                          }
                          v1121 = v1090 >> 3;
                          v1122 = v1121 + 1;
                          v1123 = v1121 + (v1121 >> 1);
                          if ( v1123 <= v1121 + 1 )
                            v1123 = v1121 + 1;
                          if ( v1121 > 0x1FFFFFFFFFFFFFFFLL - (v1121 >> 1) )
                            v1123 = 0x1FFFFFFFFFFFFFFFLL;
                          v1124 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v1123);
                          *(_QWORD *)(v1124 + 8 * v1094) = v32;
                          v32 = v1108[37];
                          sub_141758A00(a1: v1124, a2: v1108[36], a3: (char *)v1107 - v1108[36]);
                          if ( (__int64 *)v32 != v1107 )
                            sub_141758A00(a1: v1124 + 8 * v1094 + 8, a2: v1107, a3: v1108[37] - (_QWORD)v1107);
                          v1125 = v1108[36];
                          LOBYTE(v10) = v1604;
                          if ( v1125 != 0 )
                          {
                            v1126 = v1108[38] - v1125;
                            if ( v1126 == -1 )
                              v1126 = *(unsigned int *)(v1125 - *(unsigned int *)(qword_141ABD470 + 48));
                            if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                              && (v1127 = *(_QWORD *)(qword_141ABD470 + 24),
                                  (*(_QWORD *)(qword_141ABD470 + 32) - v1127) >> 3 > v1126)
                              && (v32 = *(_QWORD *)(v1127 + 8 * v1126)) != 0 )
                            {
                              MEMORY[0x1419475D8](a1: v32 + 32, a2: v1125 - *(unsigned int *)(v32 + 120));
                              v1128 = *(_BYTE *)(v32 + 72) != 0
                                   && _InterlockedDecrement((volatile signed __int32 *)(v32 + 64)) != 0;
                              v1108 = v1603;
                              if ( !v1128 && *(_BYTE *)(v32 + 97) != 0 )
                                sub_1412D33C0(a1: v32);
                            }
                            else
                            {
                              MEMORY[0x141948990](a1: v1125 - *(unsigned int *)(qword_141ABD470 + 48));
                              v1108 = v1603;
                            }
                          }
                          v1108[36] = v1124;
                          v1108[37] = v1124 + 8 * v1122;
                          v1108[38] = v1124 + 8 * v1123;
                          a1 = v1108;
                        }
LABEL_2120:
                        v986 = v1597;
                        v1084 = v1598;
                      }
                      v985 = v1084 + 1;
                      if ( v985 >= (int)v1602 )
                        goto LABEL_499;
                      continue;
                    }
                  }
                  v319 = sub_140F74650(a1: qword_141B5FDF0, a2: LODWORD(v1587[1]));
                  if ( v319 != 0 )
                  {
                    v320 = v319;
                    v321 = (__int64 *)(v319 + 24);
                    if ( (_QWORD *)(v319 + 24) != v1587 )
                    {
                      v322 = *v321;
                      v323 = (volatile signed __int32 *)(*v321 - 4);
                      if ( *v321 == 0 )
                        v323 = nullptr;
                      v324 = (volatile signed __int32 *)(v1587[0] - 4LL);
                      if ( v1587[0] != 0 )
                      {
                        if ( v322 != 0 && _InterlockedDecrement(v323) == 0 )
                          sub_1412EC9A0(a1: v323);
                        *v321 = 0;
                        _InterlockedIncrement(v324);
                        v32 = (__int64)(v324 + 1);
                      }
                      else
                      {
                        if ( v322 != 0 && _InterlockedDecrement(v323) == 0 )
                          sub_1412EC9A0(a1: v323);
                        v32 = 0;
                      }
                      *v321 = v32;
                    }
                    *(_BYTE *)(v320 + 209) = BYTE4(v1587[1]);
                  }
                  v325 = v1587[0];
                  if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] - 4LL)) == 0 )
                    sub_1412EC9A0(a1: v325 - 4);
                  if ( ++v316 >= (int)v1602 )
                  {
                    a1 = v1603;
                    LOBYTE(v10) = v1604;
                    LOBYTE(v240) = 1;
                    goto LABEL_377;
                  }
                }
                v318 = false;
                if ( _InterlockedDecrement(v317 + 2) != 0 )
                  goto LABEL_525;
LABEL_524:
                (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v317)(a1: v317, a2: 1);
                goto LABEL_525;
              }
              v589 = (int)v1602;
              v590 = v239 & ~v1601;
              if ( v590 != 0 )
              {
                a1 = v1603;
                v591 = v1603[18];
                v592 = (v1603[19] - v591) >> 3;
                v589 = v592 + (int)v1602;
                v593 = (v1603[20] - v591) >> 3;
                LOBYTE(v10) = v1604;
                if ( v593 < v589 )
                {
                  if ( v589 >> 61 == 0 )
                  {
                    v32 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v589);
                    sub_141758A00(a1: v32, a2: a1[18], a3: a1[19] - a1[18]);
                    if ( a1[18] != 0 )
                      sub_1407E4890(a1: qword_141ABD470);
                    a1[18] = v32;
                    a1[19] = v32 + 8 * v592;
                    a1[20] = v32 + 8 * v589;
                    goto LABEL_1588;
                  }
LABEL_3119:
                  sub_1400526C0(a1: v593);
                }
              }
              else
              {
                a1 = v1603;
                v32 = v1603[18];
                v593 = (v1603[20] - v32) >> 3;
                LOBYTE(v10) = v1604;
                if ( v593 < (int)v1602 )
                {
                  if ( (int)v1602 >= 0 )
                  {
                    v834 = v1603[19];
                    v835 = v1603;
                    v836 = sub_1407E4490(a1: qword_141ABD470, a2: 8LL * (int)v1602);
                    sub_141758A00(a1: v836, a2: v835[18], a3: v835[19] - v835[18]);
                    if ( v835[18] != 0 )
                      sub_1407E4890(a1: qword_141ABD470);
                    v835[18] = v836;
                    v835[19] = v836 + v834 - v32;
                    v835[20] = v836 + 8 * v589;
                    a1 = v835;
                    goto LABEL_1588;
                  }
                  goto LABEL_3119;
                }
              }
LABEL_1588:
              if ( (int)v1602 <= 0 )
              {
                LOBYTE(v240) = 1;
                goto LABEL_377;
              }
              if ( v590 != 0 )
              {
                LODWORD(v32) = 0;
                while ( 1 )
                {
                  if ( dword_141B609C8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer
                                                     + (unsigned int)TlsIndex)
                                                   + 4LL) )
                  {
                    sub_141750E08(a1: &dword_141B609C8);
                    if ( dword_141B609C8 == -1 )
                    {
                      sub_1407E53D0(
                        a1: (unsigned int)&unk_141B60978,
                        a2: 1100150697,
                        a3: 128,
                        a4: 16,
                        a5: 0,
                        a6: 1,
                        a7: 128,
                        a8: 4096);
                      sub_141751048(a1: sub_140FE19B0);
                      sub_141750EA0(a1: &dword_141B609C8);
                    }
                  }
                  v837 = sub_1407E58C0(a1: &unk_141B60978, a2: 16);
                  *(_QWORD *)v837 = 0;
                  *(_BYTE *)(v837 + 12) = -1;
                  v838 = (_DWORD *)(v837 + 8);
                  *(_DWORD *)(v837 + 8) = 0;
                  v839 = v1595;
                  if ( v1595 != nullptr )
                    _InterlockedIncrement(v1595 + 2);
                  (*(void (__fastcall **)(volatile signed __int32 *, _DWORD *, __int64))(*(_QWORD *)v839 + 40LL))(
                    a1: v839,
                    a2: v838,
                    a3: 4);
                  if ( *((_DWORD *)v839 + 4) != 0 )
                    break;
                  sub_140814B10(a1: v839, a2: v1587, a3: v837);
                  if ( LODWORD(v1587[0]) != 0 )
                    break;
                  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v839 + 40LL))(
                    a1: v839,
                    a2: v837 + 12,
                    a3: 1);
                  LOBYTE(v589) = *((_DWORD *)v839 + 4) == 0;
                  if ( _InterlockedDecrement(v839 + 2) == 0 )
                    goto LABEL_1597;
LABEL_1598:
                  if ( (_BYTE)v589 == 0 )
                    goto LABEL_375;
                  v1598 = v837;
                  LODWORD(v1597) = v32;
                  LODWORD(v1599) = v589;
                  v840 = v1603[18];
                  v841 = (unsigned __int64 *)v1603[19];
                  v842 = (__int64)v841 - v840;
                  v843 = (unsigned __int64 *)v840;
                  if ( (__int64)v841 - v840 > 0 )
                  {
                    v589 = (unsigned __int64)v842 >> 3;
                    v843 = (unsigned __int64 *)v1603[18];
                    v844 = (unsigned __int64)v842 >> 3;
                    do
                    {
                      v844 = (unsigned __int64)v844 >> 1;
                      if ( *(_DWORD *)(v843[v844] + 8) < *v838 )
                      {
                        v843 += v844 + 1;
                        v844 = v589 + ~v844;
                      }
                      v589 = v844;
                    }
                    while ( v844 > 0 );
                  }
                  if ( v843 == v841 )
                  {
                    a1 = v1603;
                    if ( v841 == (unsigned __int64 *)v1603[20] )
                    {
                      v850 = v1603;
                      v851 = (v842 >> 3) + 1;
                      v852 = (unsigned __int64)(v842 >> 3) >> 1;
                      v853 = 0x1FFFFFFFFFFFFFFFLL - v852;
                      v589 = (v842 >> 3) + v852;
                      if ( v589 <= v851 )
                        v589 = (v842 >> 3) + 1;
                      if ( v842 >> 3 > v853 )
                        v589 = 0x1FFFFFFFFFFFFFFFLL;
                      v854 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v589);
                      *(_QWORD *)(v854 + v842) = v1598;
                      v10 = v850[19];
                      sub_141758A00(a1: v854, a2: v850[18], a3: (char *)v841 - v850[18]);
                      v390 = v10 == (_QWORD)v841;
                      LOBYTE(v10) = v1604;
                      if ( !v390 )
                        sub_141758A00(a1: v854 + v842 + 8, a2: v841, a3: v850[19] - (_QWORD)v841);
                      v855 = v850[18];
                      if ( v855 != 0 )
                      {
                        v10 = (__int64)v850;
                        v856 = v850[20] - v855;
                        if ( v856 == -1 )
                          v856 = *(unsigned int *)(v855 - *(unsigned int *)(qword_141ABD470 + 48));
                        if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                          && (v857 = *(_QWORD *)(qword_141ABD470 + 24),
                              (*(_QWORD *)(qword_141ABD470 + 32) - v857) >> 3 > v856)
                          && (v858 = *(_QWORD *)(v857 + 8 * v856)) != 0 )
                        {
                          MEMORY[0x1419475D8](a1: v858 + 32, a2: v855 - *(unsigned int *)(v858 + 120));
                          v859 = *(_BYTE *)(v858 + 72) != 0
                              && _InterlockedDecrement((volatile signed __int32 *)(v858 + 64)) != 0;
                          v850 = (_QWORD *)v10;
                          LOBYTE(v10) = v1604;
                          if ( !v859 && *(_BYTE *)(v858 + 97) != 0 )
                            sub_1412D33C0(a1: v858);
                        }
                        else
                        {
                          MEMORY[0x141948990](a1: v855 - *(unsigned int *)(qword_141ABD470 + 48));
                          v850 = (_QWORD *)v10;
                          LOBYTE(v10) = v1604;
                        }
                      }
                      v850[18] = v854;
                      v850[19] = v854 + 8 * v851;
                      v850[20] = v854 + 8 * v589;
                      a1 = v850;
                      goto LABEL_1674;
                    }
LABEL_1633:
                    *v841 = v1598;
                    a1[19] += 8LL;
                    goto LABEL_1673;
                  }
                  v845 = ((__int64)v843 - v840) >> 3;
                  if ( *(_DWORD *)(*v843 + 8) == *v838 )
                  {
                    v846 = v842 >> 3;
                    v847 = v1603;
                    if ( v846 > v845 )
                    {
                      v589 = *(_QWORD *)(v840 + 8 * v845);
                      if ( v589 != 0 )
                      {
                        v848 = *(_QWORD *)v589;
                        if ( *(_QWORD *)v589 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v848 - 4)) == 0 )
                          sub_1412EC9A0(a1: v848 - 4);
                        sub_140FE1850(a1: v589);
                        v840 = v847[18];
                        v841 = (unsigned __int64 *)v847[19];
                        v846 = ((__int64)v841 - v840) >> 3;
                      }
                    }
                    if ( v846 <= v845 )
                    {
                      v849 = v845 + 1;
                      v589 = v845 + 1 - v846;
                      if ( v845 + 1 >= v846 )
                      {
                        if ( v845 + 1 > v846 )
                        {
                          v867 = v1603;
                          v868 = (v1603[20] - v840) >> 3;
                          if ( v868 >= v849 )
                          {
                            v875 = &v841[v589];
                            v589 *= 8LL;
                            sub_141758A10(a1: v841, a2: 0, a3: v589);
                            v867[19] = v875;
                            v840 = v867[18];
                          }
                          else
                          {
                            v593 = v849 >> 61;
                            if ( v849 >> 61 != 0 )
                              goto LABEL_3119;
                            v869 = v868 + (v868 >> 1);
                            if ( v869 <= v849 )
                              v869 = v845 + 1;
                            if ( v868 > 0x1FFFFFFFFFFFFFFFLL - (v868 >> 1) )
                              v869 = 0x1FFFFFFFFFFFFFFFLL;
                            v840 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v869);
                            sub_141758A10(a1: v840 + 8 * v846, a2: 0, a3: 8 * v589);
                            v589 = (unsigned __int64)v1603;
                            sub_141758A00(a1: v840, a2: v1603[18], a3: v1603[19] - v1603[18]);
                            v870 = *(_QWORD *)(v589 + 144);
                            if ( v870 != 0 )
                            {
                              v871 = *(_QWORD *)(v589 + 160) - v870;
                              if ( v871 == -1 )
                                v871 = *(unsigned int *)(v870 - *(unsigned int *)(qword_141ABD470 + 48));
                              if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                                && (v872 = *(_QWORD *)(qword_141ABD470 + 24),
                                    (*(_QWORD *)(qword_141ABD470 + 32) - v872) >> 3 > v871)
                                && (v873 = *(_QWORD *)(v872 + 8 * v871)) != 0 )
                              {
                                MEMORY[0x1419475D8](a1: v873 + 32, a2: v870 - *(unsigned int *)(v873 + 120));
                                v874 = *(_BYTE *)(v873 + 72) != 0
                                    && _InterlockedDecrement((volatile signed __int32 *)(v873 + 64)) != 0;
                                v589 = (unsigned __int64)v1603;
                                if ( !v874 && *(_BYTE *)(v873 + 97) != 0 )
                                  sub_1412D33C0(a1: v873);
                              }
                              else
                              {
                                MEMORY[0x141948990](a1: v870 - *(unsigned int *)(qword_141ABD470 + 48));
                                v589 = (unsigned __int64)v1603;
                              }
                            }
                            *(_QWORD *)(v589 + 144) = v840;
                            *(_QWORD *)(v589 + 152) = v840 + 8 * v849;
                            *(_QWORD *)(v589 + 160) = v840 + 8 * v869;
                          }
                        }
                      }
                      else
                      {
                        v1603[19] = v840 + 8 * v849;
                      }
                    }
                    *(_QWORD *)(v840 + 8 * v845) = v1598;
                    a1 = v1603;
                    goto LABEL_1673;
                  }
                  v589 = v840 + 8 * v845;
                  v10 = (__int64)v1603;
                  if ( v841 == (unsigned __int64 *)v1603[20] )
                  {
                    v860 = v842 >> 3;
                    v861 = v860 + (v860 >> 1);
                    v1574 = v860 + 1;
                    if ( v861 <= v860 + 1 )
                      v861 = v860 + 1;
                    if ( v860 > 0x1FFFFFFFFFFFFFFFLL - (v860 >> 1) )
                      v861 = 0x1FFFFFFFFFFFFFFFLL;
                    v862 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v861);
                    *(_QWORD *)(v862 + 8 * v845) = v1598;
                    v863 = *(_QWORD *)(v10 + 152);
                    sub_141758A00(a1: v862, a2: *(_QWORD *)(v10 + 144), a3: v589 - *(_QWORD *)(v10 + 144));
                    if ( v863 != v589 )
                      sub_141758A00(a1: v862 + 8 * v845 + 8, a2: v589, a3: *(_QWORD *)(v10 + 152) - v589);
                    v864 = *(_QWORD *)(v10 + 144);
                    LOBYTE(v240) = v1599;
                    if ( v864 != 0 )
                    {
                      v865 = *(_QWORD *)(v10 + 160) - v864;
                      if ( v865 == -1 )
                        v865 = *(unsigned int *)(v864 - *(unsigned int *)(qword_141ABD470 + 48));
                      if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                        && (v589 = *(_QWORD *)(qword_141ABD470 + 24),
                            (__int64)(*(_QWORD *)(qword_141ABD470 + 32) - v589) >> 3 > v865)
                        && (v589 = *(_QWORD *)(v589 + 8 * v865)) != 0 )
                      {
                        MEMORY[0x1419475D8](a1: v589 + 32, a2: v864 - *(unsigned int *)(v589 + 120));
                        v866 = *(_BYTE *)(v589 + 72) != 0
                            && _InterlockedDecrement((volatile signed __int32 *)(v589 + 64)) != 0;
                        v10 = (__int64)v1603;
                        if ( !v866 && *(_BYTE *)(v589 + 97) != 0 )
                          sub_1412D33C0(a1: v589);
                      }
                      else
                      {
                        MEMORY[0x141948990](a1: v864 - *(unsigned int *)(qword_141ABD470 + 48));
                        v10 = (__int64)v1603;
                      }
                    }
                    *(_QWORD *)(v10 + 144) = v862;
                    *(_QWORD *)(v10 + 152) = v862 + 8 * v1574;
                    *(_QWORD *)(v10 + 160) = v862 + 8 * v861;
                    a1 = (_QWORD *)v10;
                    LOBYTE(v10) = v1604;
                    goto LABEL_1675;
                  }
                  a1 = v1603;
                  if ( v841 == (unsigned __int64 *)v589 )
                    goto LABEL_1633;
                  *v841 = *(v841 - 1);
                  *(_QWORD *)(v10 + 152) += 8LL;
                  sub_141758A00(a1: v589 + 8, a2: v589, a3: (char *)v841 - v589 - 8);
                  *(_QWORD *)v589 = v1598;
LABEL_1673:
                  LOBYTE(v10) = v1604;
LABEL_1674:
                  LOBYTE(v240) = v1599;
LABEL_1675:
                  LODWORD(v32) = v1597 + 1;
                  if ( (int)v1597 + 1 >= (int)v1602 )
                    goto LABEL_377;
                }
                LODWORD(v589) = 0;
                if ( _InterlockedDecrement(v839 + 2) != 0 )
                  goto LABEL_1598;
LABEL_1597:
                (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v839)(a1: v839, a2: 1);
                goto LABEL_1598;
              }
              v1041 = 0;
              while ( 1 )
              {
                if ( dword_141B609C8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer
                                                   + (unsigned int)TlsIndex)
                                                 + 4LL) )
                {
                  sub_141750E08(a1: &dword_141B609C8);
                  if ( dword_141B609C8 == -1 )
                  {
                    sub_1407E53D0(
                      a1: (unsigned int)&unk_141B60978,
                      a2: 1100150697,
                      a3: 128,
                      a4: 16,
                      a5: 0,
                      a6: 1,
                      a7: 128,
                      a8: 4096);
                    sub_141751048(a1: sub_140FE19B0);
                    sub_141750EA0(a1: &dword_141B609C8);
                  }
                }
                v1042 = sub_1407E58C0(a1: &unk_141B60978, a2: 16);
                *(_QWORD *)v1042 = 0;
                *(_BYTE *)(v1042 + 12) = -1;
                *(_DWORD *)(v1042 + 8) = 0;
                v1043 = v1595;
                if ( v1595 != nullptr )
                  _InterlockedIncrement(v1595 + 2);
                (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v1043 + 40LL))(
                  a1: v1043,
                  a2: v1042 + 8,
                  a3: 4);
                if ( *((_DWORD *)v1043 + 4) != 0 )
                  break;
                sub_140814B10(a1: v1043, a2: v1587, a3: v1042);
                if ( LODWORD(v1587[0]) != 0 )
                  break;
                (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v1043 + 40LL))(
                  a1: v1043,
                  a2: v1042 + 12,
                  a3: 1);
                LOBYTE(v240) = *((_DWORD *)v1043 + 4) == 0;
                if ( _InterlockedDecrement(v1043 + 2) == 0 )
                  goto LABEL_2033;
LABEL_2034:
                if ( (_BYTE)v240 != 0 )
                {
                  v32 = a1[19];
                  if ( v32 == a1[20] )
                  {
                    LODWORD(v1598) = v1041;
                    LODWORD(v1599) = v240;
                    v1044 = v32 - a1[18];
                    v1045 = v1044 >> 3;
                    v10 = (__int64)a1;
                    v1046 = (unsigned __int64)(v1044 >> 3) >> 1;
                    v1047 = 0x1FFFFFFFFFFFFFFFLL - v1046;
                    v1048 = (v1044 >> 3) + v1046;
                    v1597 = (v1044 >> 3) + 1;
                    if ( v1048 <= v1597 )
                      v1048 = v1045 + 1;
                    if ( v1045 > v1047 )
                      v1048 = 0x1FFFFFFFFFFFFFFFLL;
                    v1049 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v1048);
                    *(_QWORD *)(v1049 + v1044) = v1042;
                    v1050 = *(_QWORD *)(v10 + 152);
                    sub_141758A00(a1: v1049, a2: *(_QWORD *)(v10 + 144), a3: v32 - *(_QWORD *)(v10 + 144));
                    if ( v1050 != v32 )
                      sub_141758A00(a1: v1049 + v1044 + 8, a2: v32, a3: *(_QWORD *)(v10 + 152) - v32);
                    v1051 = *(_QWORD *)(v10 + 144);
                    v240 = v1599;
                    v1041 = v1598;
                    if ( v1051 != 0 )
                    {
                      v1052 = *(_QWORD *)(v10 + 160) - v1051;
                      if ( v1052 == -1 )
                        v1052 = *(unsigned int *)(v1051 - *(unsigned int *)(qword_141ABD470 + 48));
                      if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                        && (v1053 = *(_QWORD *)(qword_141ABD470 + 24),
                            (*(_QWORD *)(qword_141ABD470 + 32) - v1053) >> 3 > v1052)
                        && (v32 = *(_QWORD *)(v1053 + 8 * v1052)) != 0 )
                      {
                        MEMORY[0x1419475D8](a1: v32 + 32, a2: v1051 - *(unsigned int *)(v32 + 120));
                        v1054 = *(_BYTE *)(v32 + 72) != 0
                             && _InterlockedDecrement((volatile signed __int32 *)(v32 + 64)) != 0;
                        v10 = (__int64)v1603;
                        if ( !v1054 && *(_BYTE *)(v32 + 97) != 0 )
                          sub_1412D33C0(a1: v32);
                      }
                      else
                      {
                        MEMORY[0x141948990](a1: v1051 - *(unsigned int *)(qword_141ABD470 + 48));
                        v10 = (__int64)v1603;
                      }
                    }
                    *(_QWORD *)(v10 + 144) = v1049;
                    *(_QWORD *)(v10 + 152) = v1049 + 8 * v1597;
                    *(_QWORD *)(v10 + 160) = v1049 + 8 * v1048;
                    a1 = (_QWORD *)v10;
                    LOBYTE(v10) = v1604;
                  }
                  else
                  {
                    *(_QWORD *)v32 = v1042;
                    a1[19] += 8LL;
                  }
                  if ( ++v1041 < (int)v1602 )
                    continue;
                }
                goto LABEL_377;
              }
              v240 = 0;
              if ( _InterlockedDecrement(v1043 + 2) != 0 )
                goto LABEL_2034;
LABEL_2033:
              (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v1043)(a1: v1043, a2: 1);
              goto LABEL_2034;
            }
            v399 = (int)v1602;
            v400 = v178;
            if ( v178 )
            {
              v245 = *(_QWORD *)v10;
              v401 = (__int64)(*(_QWORD *)(v10 + 8) - *(_QWORD *)v10) >> 3;
              v402 = v401 + (int)v1602;
              v403 = (__int64)(*(_QWORD *)(v10 + 16) - *(_QWORD *)v10) >> 3;
              LOBYTE(v10) = v1604;
              if ( v403 < v402 )
              {
                if ( v402 >> 61 == 0 )
                {
                  v32 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v402);
                  sub_141758A00(a1: v32, a2: *a1, a3: a1[1] - *a1);
                  if ( *a1 != 0 )
                    sub_1407E4890(a1: qword_141ABD470);
                  *a1 = v32;
                  a1[1] = v32 + 8 * v401;
                  v245 = v32 + 8 * v402;
                  a1[2] = v245;
                  goto LABEL_1248;
                }
LABEL_3117:
                sub_1400526C0(a1: v403);
              }
            }
            else
            {
              v32 = *(_QWORD *)v10;
              v403 = (__int64)(*(_QWORD *)(v10 + 16) - *(_QWORD *)v10) >> 3;
              LOBYTE(v10) = v1604;
              if ( v403 < (int)v1602 )
              {
                if ( (int)v1602 >= 0 )
                {
                  v674 = a1[1];
                  v675 = a1;
                  v676 = sub_1407E4490(a1: qword_141ABD470, a2: 8LL * (int)v1602);
                  sub_141758A00(a1: v676, a2: *v675, a3: v675[1] - *v675);
                  if ( *v675 != 0 )
                    sub_1407E4890(a1: qword_141ABD470);
                  *v675 = v676;
                  v675[1] = v676 + v674 - v32;
                  v245 = v676 + 8 * v399;
                  v675[2] = v245;
                  a1 = v675;
                  goto LABEL_1248;
                }
                goto LABEL_3117;
              }
            }
LABEL_1248:
            if ( (int)v1602 <= 0 )
            {
              LOBYTE(v245) = 1;
              LODWORD(v1599) = v245;
              goto LABEL_276;
            }
            v677 = 0;
            if ( !v400 )
            {
              v929 = v1597;
              do
              {
                if ( dword_141B60BD8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer
                                                   + (unsigned int)TlsIndex)
                                                 + 4LL) )
                {
                  sub_141750E08(a1: &dword_141B60BD8);
                  if ( dword_141B60BD8 == -1 )
                  {
                    sub_1407E53D0(
                      a1: (unsigned int)&unk_141B60B88,
                      a2: 1100150715,
                      a3: 1024,
                      a4: 32,
                      a5: 0,
                      a6: 1,
                      a7: 1024,
                      a8: 4096);
                    sub_141751048(a1: sub_140FE2250);
                    sub_141750EA0(a1: &dword_141B60BD8);
                  }
                }
                v930 = sub_1407E58C0(a1: &unk_141B60B88, a2: 32);
                *(_QWORD *)v930 = 0;
                *(_QWORD *)(v930 + 8) = 0;
                *(_QWORD *)(v930 + 16) = 0;
                *(_DWORD *)(v930 + 24) = 0;
                *(_WORD *)(v930 + 28) = -1;
                v1587[0] = v1595;
                if ( v1595 != nullptr )
                  _InterlockedIncrement(v1595 + 2);
                v931 = sub_140E498B0(a1: v930, a2: v1587, a3: v929);
                v932 = (void (__fastcall ***)(_QWORD, __int64))v1587[0];
                if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] + 8LL)) == 0 )
                  (**v932)(a1: v932, a2: 1);
                LODWORD(v1599) = v931;
                if ( (_BYTE)v931 == 0 )
                  break;
                v32 = a1[1];
                if ( v32 == a1[2] )
                {
                  v933 = v32 - *a1;
                  v934 = v933 >> 3;
                  v10 = (__int64)a1;
                  v935 = (unsigned __int64)(v933 >> 3) >> 1;
                  v936 = 0x1FFFFFFFFFFFFFFFLL - v935;
                  v937 = (v933 >> 3) + v935;
                  v1598 = (v933 >> 3) + 1;
                  if ( v937 <= v1598 )
                    v937 = v934 + 1;
                  if ( v934 > v936 )
                    v937 = 0x1FFFFFFFFFFFFFFFLL;
                  v938 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v937);
                  *(_QWORD *)(v938 + v933) = v930;
                  v939 = *(_QWORD *)(v10 + 8);
                  sub_141758A00(a1: v938, a2: *(_QWORD *)v10, a3: v32 - *(_QWORD *)v10);
                  if ( v939 != v32 )
                    sub_141758A00(a1: v938 + v933 + 8, a2: v32, a3: *(_QWORD *)(v10 + 8) - v32);
                  v940 = *(_QWORD *)v10;
                  v929 = v1597;
                  if ( *(_QWORD *)v10 != 0 )
                  {
                    v941 = *(_QWORD *)(v10 + 16) - v940;
                    if ( v941 == -1 )
                      v941 = *(unsigned int *)(v940 - *(unsigned int *)(qword_141ABD470 + 48));
                    if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                      && (v942 = *(_QWORD *)(qword_141ABD470 + 24),
                          (*(_QWORD *)(qword_141ABD470 + 32) - v942) >> 3 > v941)
                      && (v32 = *(_QWORD *)(v942 + 8 * v941)) != 0 )
                    {
                      MEMORY[0x1419475D8](a1: v32 + 32, a2: v940 - *(unsigned int *)(v32 + 120));
                      v943 = *(_BYTE *)(v32 + 72) != 0
                          && _InterlockedDecrement((volatile signed __int32 *)(v32 + 64)) != 0;
                      v10 = (__int64)v1603;
                      if ( !v943 && *(_BYTE *)(v32 + 97) != 0 )
                        sub_1412D33C0(a1: v32);
                    }
                    else
                    {
                      MEMORY[0x141948990](a1: v940 - *(unsigned int *)(qword_141ABD470 + 48));
                      v10 = (__int64)v1603;
                    }
                  }
                  *(_QWORD *)v10 = v938;
                  *(_QWORD *)(v10 + 8) = v938 + 8 * v1598;
                  *(_QWORD *)(v10 + 16) = v938 + 8 * v937;
                  a1 = (_QWORD *)v10;
                  LOBYTE(v10) = v1604;
                }
                else
                {
                  *(_QWORD *)v32 = v930;
                  a1[1] += 8LL;
                }
                ++v677;
              }
              while ( v677 < (int)v1602 );
              goto LABEL_276;
            }
            v678 = v1597;
            while ( 1 )
            {
              if ( dword_141B60BD8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer
                                                 + (unsigned int)TlsIndex)
                                               + 4LL) )
              {
                sub_141750E08(a1: &dword_141B60BD8);
                if ( dword_141B60BD8 == -1 )
                {
                  sub_1407E53D0(
                    a1: (unsigned int)&unk_141B60B88,
                    a2: 1100150715,
                    a3: 1024,
                    a4: 32,
                    a5: 0,
                    a6: 1,
                    a7: 1024,
                    a8: 4096);
                  sub_141751048(a1: sub_140FE2250);
                  sub_141750EA0(a1: &dword_141B60BD8);
                }
              }
              v32 = sub_1407E58C0(a1: &unk_141B60B88, a2: 32);
              *(_QWORD *)v32 = 0;
              *(_QWORD *)(v32 + 8) = 0;
              *(_QWORD *)(v32 + 16) = 0;
              *(_DWORD *)(v32 + 24) = 0;
              *(_WORD *)(v32 + 28) = -1;
              v1587[0] = v1595;
              if ( v1595 != nullptr )
                _InterlockedIncrement(v1595 + 2);
              v777 = sub_140E498B0(a1: v32, a2: v1587, a3: v678);
              v778 = (void (__fastcall ***)(_QWORD, __int64))v1587[0];
              if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] + 8LL)) == 0 )
                (**v778)(a1: v778, a2: 1);
              if ( (_BYTE)v777 == 0 )
              {
                LODWORD(v1599) = 0;
                goto LABEL_276;
              }
              LODWORD(v1598) = v677;
              LODWORD(v1599) = v777;
              v779 = *a1;
              v780 = (__int64)a1;
              v781 = (__int64 *)a1[1];
              v782 = (__int64)v781 - v779;
              v783 = (__int64 *)v779;
              if ( (__int64)v781 - v779 > 0 )
              {
                v784 = (unsigned __int64)v782 >> 3;
                v783 = (__int64 *)v779;
                v785 = (unsigned __int64)v782 >> 3;
                do
                {
                  v785 = (unsigned __int64)v785 >> 1;
                  if ( *(_DWORD *)(v783[v785] + 24) < *(_DWORD *)(v32 + 24) )
                  {
                    v783 += v785 + 1;
                    v785 = v784 + ~v785;
                  }
                  v784 = v785;
                }
                while ( v785 > 0 );
              }
              if ( v783 == v781 )
              {
                if ( v781 == *(__int64 **)(v780 + 16) )
                {
                  v10 = v780;
                  v805 = (unsigned __int64)(v782 >> 3) >> 1;
                  v806 = 0x1FFFFFFFFFFFFFFFLL - v805;
                  v807 = (v782 >> 3) + v805;
                  if ( v807 <= (v782 >> 3) + 1 )
                    v807 = (v782 >> 3) + 1;
                  if ( v782 >> 3 > v806 )
                    v807 = 0x1FFFFFFFFFFFFFFFLL;
                  v808 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v807);
                  *(_QWORD *)(v808 + v782) = v32;
                  v809 = *(__int64 **)(v10 + 8);
                  sub_141758A00(a1: v808, a2: *(_QWORD *)v10, a3: (char *)v781 - *(_QWORD *)v10);
                  if ( v809 != v781 )
                    sub_141758A00(a1: v808 + v782 + 8, a2: v781, a3: *(_QWORD *)(v10 + 8) - (_QWORD)v781);
                  v810 = v808;
                  v811 = *(_QWORD *)v10;
                  v678 = v1597;
                  if ( *(_QWORD *)v10 != 0 )
                  {
                    v812 = *(_QWORD *)(v10 + 16) - v811;
                    if ( v812 == -1 )
                      v812 = *(unsigned int *)(v811 - *(unsigned int *)(qword_141ABD470 + 48));
                    if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                      && (v813 = *(_QWORD *)(qword_141ABD470 + 24),
                          (*(_QWORD *)(qword_141ABD470 + 32) - v813) >> 3 > v812)
                      && (v32 = *(_QWORD *)(v813 + 8 * v812)) != 0 )
                    {
                      MEMORY[0x1419475D8](a1: v32 + 32, a2: v811 - *(unsigned int *)(v32 + 120));
                      v814 = *(_BYTE *)(v32 + 72) != 0
                          && _InterlockedDecrement((volatile signed __int32 *)(v32 + 64)) != 0;
                      v10 = (__int64)v1603;
                      if ( !v814 && *(_BYTE *)(v32 + 97) != 0 )
                        sub_1412D33C0(a1: v32);
                    }
                    else
                    {
                      MEMORY[0x141948990](a1: v811 - *(unsigned int *)(qword_141ABD470 + 48));
                      v10 = (__int64)v1603;
                    }
                  }
                  *(_QWORD *)v10 = v810;
                  *(_QWORD *)(v10 + 8) = v810 + 8 * ((v782 >> 3) + 1);
                  *(_QWORD *)(v10 + 16) = v810 + 8 * v807;
                  a1 = (_QWORD *)v10;
                  LOBYTE(v10) = v1604;
                  goto LABEL_1462;
                }
                *v781 = v32;
                *(_QWORD *)(v780 + 8) += 8LL;
                a1 = (_QWORD *)v780;
              }
              else
              {
                v786 = ((__int64)v783 - v779) >> 3;
                if ( *(_DWORD *)(*v783 + 24) == *(_DWORD *)(v32 + 24) )
                {
                  v787 = v782 >> 3;
                  if ( v787 > v786 )
                  {
                    v788 = *(__int64 **)(v779 + 8 * v786);
                    if ( v788 != nullptr )
                    {
                      sub_140E44A40(a1: v788 + 2);
                      v789 = v788[1];
                      if ( v789 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v789 - 4)) == 0 )
                        sub_1412EC9A0(a1: v789 - 4);
                      v790 = *v788;
                      if ( *v788 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v790 - 4)) == 0 )
                        sub_1412EC9A0(a1: v790 - 4);
                      sub_140FE20F0(a1: v788);
                      v779 = *v1603;
                      v781 = (__int64 *)v1603[1];
                      v787 = ((__int64)v781 - *v1603) >> 3;
                    }
                  }
                  if ( v787 <= v786 )
                  {
                    v791 = v786 + 1;
                    v792 = v786 + 1 - v787;
                    if ( v786 + 1 < v787 )
                    {
                      v1603[1] = v779 + 8 * v791;
                    }
                    else if ( v786 + 1 > v787 )
                    {
                      v793 = v1603;
                      v794 = (v1603[2] - v779) >> 3;
                      if ( v794 >= v791 )
                      {
                        v825 = &v781[v792];
                        sub_141758A10(a1: v781, a2: 0, a3: 8 * v792);
                        v793[1] = (__int64)v825;
                        v779 = *v793;
                      }
                      else
                      {
                        v403 = v791 >> 61;
                        if ( v791 >> 61 != 0 )
                          goto LABEL_3117;
                        v795 = v794 + (v794 >> 1);
                        if ( v795 <= v791 )
                          v795 = v786 + 1;
                        if ( v794 > 0x1FFFFFFFFFFFFFFFLL - (v794 >> 1) )
                          v795 = 0x1FFFFFFFFFFFFFFFLL;
                        v779 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v795);
                        sub_141758A10(a1: v779 + 8 * v787, a2: 0, a3: 8 * (v786 + 1 - v787));
                        v796 = v1603;
                        sub_141758A00(a1: v779, a2: *v1603, a3: v1603[1] - *v1603);
                        v797 = *v796;
                        if ( *v796 != 0 )
                        {
                          v798 = v796[2] - v797;
                          if ( v798 == -1 )
                            v798 = *(unsigned int *)(v797 - *(unsigned int *)(qword_141ABD470 + 48));
                          if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                            && (v799 = *(_QWORD *)(qword_141ABD470 + 24),
                                (*(_QWORD *)(qword_141ABD470 + 32) - v799) >> 3 > v798)
                            && (v800 = *(_QWORD *)(v799 + 8 * v798)) != 0 )
                          {
                            MEMORY[0x1419475D8](a1: v800 + 32, a2: v797 - *(unsigned int *)(v800 + 120));
                            v801 = *(_BYTE *)(v800 + 72) != 0
                                && _InterlockedDecrement((volatile signed __int32 *)(v800 + 64)) != 0;
                            v796 = v1603;
                            if ( !v801 && *(_BYTE *)(v800 + 97) != 0 )
                              sub_1412D33C0(a1: v800);
                          }
                          else
                          {
                            MEMORY[0x141948990](a1: v797 - *(unsigned int *)(qword_141ABD470 + 48));
                            v796 = v1603;
                          }
                        }
                        *v796 = v779;
                        v796[1] = v779 + 8 * (v786 + 1);
                        v796[2] = v779 + 8 * v795;
                      }
                      LOBYTE(v10) = v1604;
                    }
                  }
                  *(_QWORD *)(v779 + 8 * v786) = v32;
                  a1 = v1603;
                }
                else
                {
                  v802 = (__int64 *)(v779 + 8 * v786);
                  v10 = (__int64)v1603;
                  if ( v781 == (__int64 *)v1603[2] )
                  {
                    v815 = v782 >> 3;
                    v816 = v815 + 1;
                    v817 = v815 + (v815 >> 1);
                    if ( v817 <= v815 + 1 )
                      v817 = v815 + 1;
                    if ( v815 > 0x1FFFFFFFFFFFFFFFLL - (v815 >> 1) )
                      v817 = 0x1FFFFFFFFFFFFFFFLL;
                    v818 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v817);
                    *(_QWORD *)(v818 + 8 * v786) = v32;
                    v819 = *(__int64 **)(v10 + 8);
                    sub_141758A00(a1: v818, a2: *(_QWORD *)v10, a3: (char *)v802 - *(_QWORD *)v10);
                    if ( v819 != v802 )
                      sub_141758A00(a1: v818 + 8 * v786 + 8, a2: v802, a3: *(_QWORD *)(v10 + 8) - (_QWORD)v802);
                    v820 = *(_QWORD *)v10;
                    LODWORD(v32) = (unsigned __int8)v1604;
                    if ( *(_QWORD *)v10 != 0 )
                    {
                      v821 = *(_QWORD *)(v10 + 16) - v820;
                      if ( v821 == -1 )
                        v821 = *(unsigned int *)(v820 - *(unsigned int *)(qword_141ABD470 + 48));
                      if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                        && (v822 = *(_QWORD *)(qword_141ABD470 + 24),
                            (*(_QWORD *)(qword_141ABD470 + 32) - v822) >> 3 > v821)
                        && (v823 = *(_QWORD *)(v822 + 8 * v821)) != 0 )
                      {
                        MEMORY[0x1419475D8](a1: v823 + 32, a2: v820 - *(unsigned int *)(v823 + 120));
                        v824 = *(_BYTE *)(v823 + 72) != 0
                            && _InterlockedDecrement((volatile signed __int32 *)(v823 + 64)) != 0;
                        v10 = (__int64)v1603;
                        if ( !v824 && *(_BYTE *)(v823 + 97) != 0 )
                          sub_1412D33C0(a1: v823);
                      }
                      else
                      {
                        MEMORY[0x141948990](a1: v820 - *(unsigned int *)(qword_141ABD470 + 48));
                        v10 = (__int64)v1603;
                      }
                    }
                    *(_QWORD *)v10 = v818;
                    *(_QWORD *)(v10 + 8) = v818 + 8 * v816;
                    *(_QWORD *)(v10 + 16) = v818 + 8 * v817;
                    a1 = (_QWORD *)v10;
                    LOBYTE(v10) = v32;
                  }
                  else
                  {
                    if ( v781 == v802 )
                    {
                      *v781 = v32;
                      a1 = v1603;
                      v1603[1] += 8LL;
                    }
                    else
                    {
                      *v781 = *(v781 - 1);
                      v803 = v1603;
                      v1603[1] += 8LL;
                      v804 = (char *)(v781 - 1) - (char *)v802;
                      a1 = v803;
                      sub_141758A00(a1: v802 + 1, a2: v779 + 8 * v786, a3: v804);
                      *v802 = v32;
                    }
                    LOBYTE(v10) = v1604;
                  }
                }
              }
              v678 = v1597;
LABEL_1462:
              v677 = v1598 + 1;
              if ( (int)v1598 + 1 >= (int)v1602 )
                goto LABEL_276;
            }
          }
          break;
        }
        sub_140E44A40(a1: &v1587[2]);
        v1423 = v1587[1];
        if ( v1587[1] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[1] - 4LL)) == 0 )
          sub_1412EC9A0(a1: v1423 - 4);
LABEL_2834:
        LOBYTE(v739) = 0;
LABEL_2835:
        LODWORD(v10) = (unsigned __int8)v1604;
        goto LABEL_2870;
      }
      v1130 = (int)v1596;
      v1131 = v738;
      if ( v738 )
      {
        v1132 = v733[27];
        v1133 = (v733[28] - v1132) >> 3;
        v1134 = v1133 + (int)v1596;
        v1135 = (v733[29] - v1132) >> 3;
        if ( v1135 < v1134 )
        {
          if ( v1134 >> 61 == 0 )
          {
            v1136 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v1134);
            sub_141758A00(a1: v1136, a2: v733[27], a3: v733[28] - v733[27]);
            if ( v733[27] != 0 )
              sub_1407E4890(a1: qword_141ABD470);
            v733[27] = v1136;
            v733[28] = v1136 + 8 * v1133;
            v1137 = v1136 + 8 * v1134;
LABEL_2535:
            v733[29] = v1137;
            goto LABEL_2536;
          }
          goto LABEL_3125;
        }
      }
      else
      {
        v1283 = v733[27];
        v1135 = (v733[29] - v1283) >> 3;
        if ( v1135 < (int)v1596 )
        {
          if ( (int)v1596 >= 0 )
          {
            v1284 = v733[28];
            v1285 = sub_1407E4490(a1: qword_141ABD470, a2: 8LL * (int)v1596);
            sub_141758A00(a1: v1285, a2: v733[27], a3: v733[28] - v733[27]);
            if ( v733[27] != 0 )
              sub_1407E4890(a1: qword_141ABD470);
            v733[27] = v1285;
            v733[28] = v1285 + v1284 - v1283;
            v1137 = v1285 + 8 * v1130;
            goto LABEL_2535;
          }
LABEL_3125:
          sub_1400526C0(a1: v1135);
        }
      }
LABEL_2536:
      if ( (int)v1596 <= 0 )
      {
        LOBYTE(v739) = 1;
        goto LABEL_2835;
      }
      LODWORD(v10) = (unsigned __int8)v1604;
      if ( !v1131 )
      {
        v1424 = 0;
        do
        {
          v1425 = sub_141750CC0(a1: 24);
          *(_BYTE *)(v1425 + 4) = -1;
          *(_DWORD *)v1425 = 0;
          *(_QWORD *)(v1425 + 8) = 0;
          *(_QWORD *)(v1425 + 16) = 0;
          v1587[0] = v1595;
          _InterlockedIncrement(v1595 + 2);
          v1426 = v1587[0];
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v1587[0] + 40LL))(
            a1: v1587[0],
            a2: v1425,
            a3: 4);
          if ( *(_DWORD *)(v1426 + 16) != 0
            || (sub_140814B10(a1: v1587[0], a2: &v1600, a3: v1425 + 8), (_DWORD)v1600 != 0) )
          {
            LODWORD(v739) = 0;
          }
          else
          {
            LODWORD(v739) = sub_140E45290(a1: v1425 + 16, a2: v1587);
          }
          v1427 = v10;
          v1428 = (void (__fastcall ***)(_QWORD, __int64))v1587[0];
          if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] + 8LL)) == 0 )
            (**v1428)(a1: v1428, a2: 1);
          if ( (_BYTE)v739 == 0 )
            break;
          v10 = (__int64)v1603;
          v1429 = (__int64 *)v1603[28];
          if ( v1429 == (__int64 *)v1603[29] )
          {
            LODWORD(v1597) = v1424;
            LODWORD(v1599) = v739;
            v32 = (__int64)v1429 - v1603[27];
            v1430 = v32 >> 3;
            v1431 = (unsigned __int64)(v32 >> 3) >> 1;
            v1432 = 0x1FFFFFFFFFFFFFFFLL - v1431;
            v739 = (v32 >> 3) + v1431;
            v1598 = (v32 >> 3) + 1;
            if ( v739 <= v1598 )
              v739 = v1430 + 1;
            if ( v1430 > v1432 )
              v739 = 0x1FFFFFFFFFFFFFFFLL;
            v1433 = v1603;
            v1434 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v739);
            *(_QWORD *)(v1434 + v32) = v1425;
            v1435 = *(__int64 **)(v10 + 224);
            sub_141758A00(a1: v1434, a2: *(_QWORD *)(v10 + 216), a3: (char *)v1429 - *(_QWORD *)(v10 + 216));
            if ( v1435 != v1429 )
            {
              v32 += v1434 + 8;
              sub_141758A00(a1: v32, a2: v1429, a3: *(_QWORD *)(v10 + 224) - (_QWORD)v1429);
            }
            v1436 = *(_QWORD *)(v10 + 216);
            if ( v1436 != 0 )
            {
              v1437 = *(_QWORD *)(v10 + 232) - v1436;
              if ( v1437 == -1 )
                v1437 = *(unsigned int *)(v1436 - *(unsigned int *)(qword_141ABD470 + 48));
              if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                && (v1438 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v1438) >> 3 > v1437)
                && (v32 = *(_QWORD *)(v1438 + 8 * v1437)) != 0 )
              {
                MEMORY[0x1419475D8](a1: v32 + 32, a2: v1436 - *(unsigned int *)(v32 + 120));
                v1439 = *(_BYTE *)(v32 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v32 + 64)) != 0;
                v1433 = v1603;
                if ( !v1439 && *(_BYTE *)(v32 + 97) != 0 )
                  sub_1412D33C0(a1: v32);
              }
              else
              {
                MEMORY[0x141948990](a1: v1436 - *(unsigned int *)(qword_141ABD470 + 48));
                v1433 = v1603;
              }
            }
            v1433[27] = v1434;
            v1433[28] = v1434 + 8 * v1598;
            v1433[29] = v1434 + 8 * v739;
            LODWORD(v10) = (unsigned __int8)v1604;
            LOBYTE(v739) = v1599;
            v1424 = v1597;
          }
          else
          {
            *v1429 = v1425;
            *(_QWORD *)(v10 + 224) += 8LL;
            LODWORD(v10) = v1427;
          }
          ++v1424;
        }
        while ( v1424 < (int)v1596 );
        goto LABEL_2870;
      }
      v1286 = 0;
      while ( 1 )
      {
        v1379 = sub_141750CC0(a1: 24);
        *(_BYTE *)(v1379 + 4) = -1;
        *(_DWORD *)v1379 = 0;
        *(_QWORD *)(v1379 + 8) = 0;
        *(_QWORD *)(v1379 + 16) = 0;
        v1587[0] = v1595;
        _InterlockedIncrement(v1595 + 2);
        v1380 = v1587[0];
        (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v1587[0] + 40LL))(a1: v1587[0], a2: v1379, a3: 4);
        if ( *(_DWORD *)(v1380 + 16) != 0
          || (sub_140814B10(a1: v1587[0], a2: &v1600, a3: v1379 + 8), (_DWORD)v1600 != 0) )
        {
          v1381 = 0;
        }
        else
        {
          v1381 = sub_140E45290(a1: v1379 + 16, a2: v1587);
        }
        v1382 = (void (__fastcall ***)(_QWORD, __int64))v1587[0];
        if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] + 8LL)) == 0 )
          (**v1382)(a1: v1382, a2: 1);
        if ( (_BYTE)v1381 == 0 )
          goto LABEL_2834;
        LODWORD(v1597) = v1286;
        LODWORD(v1599) = v1381;
        v32 = v1603[27];
        v1383 = (__int64 *)v1603[28];
        v1384 = (__int64)v1383 - v32;
        v1385 = (__int64 *)v32;
        if ( (__int64)v1383 - v32 > 0 )
        {
          v1386 = (unsigned __int64)v1384 >> 3;
          v1385 = (__int64 *)v1603[27];
          v1387 = (unsigned __int64)v1384 >> 3;
          do
          {
            v1387 = (unsigned __int64)v1387 >> 1;
            if ( *(_DWORD *)v1385[v1387] < *(_DWORD *)v1379 )
            {
              v1385 += v1387 + 1;
              v1387 = v1386 + ~v1387;
            }
            v1386 = v1387;
          }
          while ( v1387 > 0 );
        }
        if ( v1385 == v1383 )
        {
          v1402 = v1603;
          if ( v1383 == (__int64 *)v1603[29] )
          {
            v1404 = (unsigned __int64)(v1384 >> 3) >> 1;
            v1405 = 0x1FFFFFFFFFFFFFFFLL - v1404;
            v32 = (v1384 >> 3) + v1404;
            v1598 = (v1384 >> 3) + 1;
            if ( v32 <= v1598 )
              v32 = (v1384 >> 3) + 1;
            if ( v1384 >> 3 > v1405 )
              v32 = 0x1FFFFFFFFFFFFFFFLL;
            v1406 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v32);
            *(_QWORD *)(v1406 + v1384) = v1379;
            v1407 = (__int64 *)v1402[28];
            sub_141758A00(a1: v1406, a2: v1402[27], a3: (char *)v1383 - v1402[27]);
            if ( v1407 != v1383 )
              sub_141758A00(a1: v1406 + v1384 + 8, a2: v1383, a3: v1402[28] - (_QWORD)v1383);
            v1408 = v1402[27];
            LODWORD(v10) = (unsigned __int8)v1604;
            LOBYTE(v739) = v1599;
            if ( v1408 != 0 )
            {
              v1409 = v1402[29] - v1408;
              if ( v1409 == -1 )
                v1409 = *(unsigned int *)(v1408 - *(unsigned int *)(qword_141ABD470 + 48));
              if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                && (v1410 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v1410) >> 3 > v1409)
                && (v1411 = *(_QWORD *)(v1410 + 8 * v1409)) != 0 )
              {
                MEMORY[0x1419475D8](a1: v1411 + 32, a2: v1408 - *(unsigned int *)(v1411 + 120));
                v1412 = *(_BYTE *)(v1411 + 72) != 0
                     && _InterlockedDecrement((volatile signed __int32 *)(v1411 + 64)) != 0;
                if ( !v1412 && *(_BYTE *)(v1411 + 97) != 0 )
                  sub_1412D33C0(a1: v1411);
              }
              else
              {
                MEMORY[0x141948990](a1: v1408 - *(unsigned int *)(qword_141ABD470 + 48));
              }
            }
            v1402[27] = v1406;
            v1402[28] = v1406 + 8 * v1598;
            v1402[29] = v1406 + 8 * v32;
            goto LABEL_2738;
          }
          *v1383 = v1379;
          v1402[28] += 8LL;
        }
        else
        {
          v1388 = ((__int64)v1385 - v32) >> 3;
          if ( *(_DWORD *)*v1385 == *(_DWORD *)v1379 )
          {
            v1389 = v1384 >> 3;
            if ( v1389 > v1388 )
            {
              v1390 = *(_QWORD *)(v32 + 8 * v1388);
              if ( v1390 != 0 )
              {
                sub_140E44A40(a1: v1390 + 16);
                v1391 = *(_QWORD *)(v1390 + 8);
                if ( v1391 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1391 - 4)) == 0 )
                  sub_1412EC9A0(a1: v1391 - 4);
                sub_141750CFC(a1: v1390);
                v32 = v1603[27];
                v1383 = (__int64 *)v1603[28];
                v1389 = ((__int64)v1383 - v32) >> 3;
              }
            }
            if ( v1389 <= v1388 )
            {
              v1392 = v1388 + 1;
              v1393 = v1388 + 1 - v1389;
              if ( v1388 + 1 < v1389 )
              {
                v1603[28] = v32 + 8 * v1392;
              }
              else if ( v1388 + 1 > v1389 )
              {
                v1394 = (v1603[29] - v32) >> 3;
                if ( v1394 >= v1392 )
                {
                  v1421 = v1603;
                  sub_141758A10(a1: v1383, a2: 0, a3: 8 * v1393);
                  v1421[28] = &v1383[v1393];
                  v32 = v1421[27];
                }
                else
                {
                  v1135 = v1392 >> 61;
                  if ( v1392 >> 61 != 0 )
                    goto LABEL_3125;
                  v1395 = v1394 + (v1394 >> 1);
                  v1598 = v1388 + 1;
                  if ( v1395 <= v1392 )
                    v1395 = v1388 + 1;
                  if ( v1394 > 0x1FFFFFFFFFFFFFFFLL - (v1394 >> 1) )
                    v1395 = 0x1FFFFFFFFFFFFFFFLL;
                  v32 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v1395);
                  sub_141758A10(a1: v32 + 8 * v1389, a2: 0, a3: 8 * v1393);
                  v1396 = v1603;
                  sub_141758A00(a1: v32, a2: v1603[27], a3: v1603[28] - v1603[27]);
                  v1397 = v1396[27];
                  if ( v1397 != 0 )
                  {
                    v1398 = v1603[29] - v1397;
                    if ( v1398 == -1 )
                      v1398 = *(unsigned int *)(v1397 - *(unsigned int *)(qword_141ABD470 + 48));
                    if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                      && (v1399 = *(_QWORD *)(qword_141ABD470 + 24),
                          (*(_QWORD *)(qword_141ABD470 + 32) - v1399) >> 3 > v1398)
                      && (v1400 = *(_QWORD *)(v1399 + 8 * v1398)) != 0 )
                    {
                      MEMORY[0x1419475D8](a1: v1400 + 32, a2: v1397 - *(unsigned int *)(v1400 + 120));
                      v1401 = *(_BYTE *)(v1400 + 72) != 0
                           && _InterlockedDecrement((volatile signed __int32 *)(v1400 + 64)) != 0;
                      if ( !v1401 && *(_BYTE *)(v1400 + 97) != 0 )
                        sub_1412D33C0(a1: v1400);
                    }
                    else
                    {
                      MEMORY[0x141948990](a1: v1397 - *(unsigned int *)(qword_141ABD470 + 48));
                    }
                  }
                  v1422 = v1603;
                  v1603[27] = v32;
                  v1422[28] = v32 + 8 * v1598;
                  v1422[29] = v32 + 8 * v1395;
                }
              }
            }
            *(_QWORD *)(v32 + 8 * v1388) = v1379;
          }
          else
          {
            v32 += 8 * v1388;
            v1403 = v1603;
            if ( v1383 == (__int64 *)v1603[29] )
            {
              v1413 = v1384 >> 3;
              v1414 = v1413 + (v1413 >> 1);
              v1598 = v1413 + 1;
              if ( v1414 <= v1413 + 1 )
                v1414 = v1413 + 1;
              if ( v1413 > 0x1FFFFFFFFFFFFFFFLL - (v1413 >> 1) )
                v1414 = 0x1FFFFFFFFFFFFFFFLL;
              v1415 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v1414);
              *(_QWORD *)(v1415 + 8 * v1388) = v1379;
              v1416 = v1403[28];
              sub_141758A00(a1: v1415, a2: v1403[27], a3: v32 - v1403[27]);
              if ( v1416 != v32 )
                sub_141758A00(a1: v1415 + 8 * v1388 + 8, a2: v32, a3: v1403[28] - v32);
              v1417 = v1403[27];
              LODWORD(v10) = (unsigned __int8)v1604;
              if ( v1417 != 0 )
              {
                v1418 = v1403[29] - v1417;
                if ( v1418 == -1 )
                  v1418 = *(unsigned int *)(v1417 - *(unsigned int *)(qword_141ABD470 + 48));
                if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                  && (v1419 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v1419) >> 3 > v1418)
                  && (v32 = *(_QWORD *)(v1419 + 8 * v1418)) != 0 )
                {
                  MEMORY[0x1419475D8](a1: v32 + 32, a2: v1417 - *(unsigned int *)(v32 + 120));
                  v1420 = *(_BYTE *)(v32 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v32 + 64)) != 0;
                  v1403 = v1603;
                  LODWORD(v10) = (unsigned __int8)v1604;
                  if ( !v1420 && *(_BYTE *)(v32 + 97) != 0 )
                    sub_1412D33C0(a1: v32);
                }
                else
                {
                  MEMORY[0x141948990](a1: v1417 - *(unsigned int *)(qword_141ABD470 + 48));
                }
              }
              v1403[27] = v1415;
              v1403[28] = v1415 + 8 * v1598;
              v1403[29] = v1415 + 8 * v1414;
              goto LABEL_2737;
            }
            if ( v1383 == (__int64 *)v32 )
            {
              *v1383 = v1379;
              v1603[28] += 8LL;
            }
            else
            {
              *v1383 = *(v1383 - 1);
              v1603[28] += 8LL;
              sub_141758A00(a1: v32 + 8, a2: v32, a3: (char *)v1383 - v32 - 8);
              *(_QWORD *)v32 = v1379;
            }
          }
        }
        LODWORD(v10) = (unsigned __int8)v1604;
LABEL_2737:
        LOBYTE(v739) = v1599;
LABEL_2738:
        v1286 = v1597 + 1;
        if ( (int)v1597 + 1 >= (int)v1596 )
          goto LABEL_2870;
      }
    }
    v977 = (int)v1602;
    v978 = v529;
    if ( v529 )
    {
      v740 = a1[33];
      v979 = (a1[34] - v740) >> 3;
      v980 = v979 + (int)v1602;
      v981 = (a1[35] - v740) >> 3;
      if ( v981 < v980 )
      {
        if ( v980 >> 61 == 0 )
        {
          v32 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v980);
          sub_141758A00(a1: v32, a2: a1[33], a3: a1[34] - a1[33]);
          if ( a1[33] != 0 )
            sub_1407E4890(a1: qword_141ABD470);
          a1[33] = v32;
          a1[34] = v32 + 8 * v979;
          v740 = v32 + 8 * v980;
          a1[35] = v740;
          goto LABEL_2269;
        }
LABEL_3123:
        sub_1400526C0(a1: v981);
      }
    }
    else
    {
      v32 = a1[33];
      v981 = (a1[35] - v32) >> 3;
      if ( v981 < (int)v1602 )
      {
        if ( (int)v1602 >= 0 )
        {
          v1158 = a1[34];
          v1159 = a1;
          v1160 = sub_1407E4490(a1: qword_141ABD470, a2: 8LL * (int)v1602);
          sub_141758A00(a1: v1160, a2: v1159[33], a3: v1159[34] - v1159[33]);
          if ( v1159[33] != 0 )
            sub_1407E4890(a1: qword_141ABD470);
          v1159[33] = v1160;
          v1159[34] = v1160 + v1158 - v32;
          v740 = v1160 + 8 * v977;
          v1159[35] = v740;
          a1 = v1159;
          goto LABEL_2269;
        }
        goto LABEL_3123;
      }
    }
LABEL_2269:
    if ( (int)v1602 <= 0 )
    {
      LOBYTE(v740) = 1;
      LODWORD(v1599) = v740;
      goto LABEL_946;
    }
    v1161 = 0;
    if ( !v978 )
    {
      v1341 = v1597;
      do
      {
        if ( dword_141B608C0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                         + 4LL) )
        {
          sub_141750E08(a1: &dword_141B608C0);
          if ( dword_141B608C0 == -1 )
          {
            sub_1407E53D0(
              a1: (unsigned int)&unk_141B60870,
              a2: 1100150681,
              a3: 256,
              a4: 40,
              a5: 0,
              a6: 1,
              a7: 256,
              a8: 4096);
            sub_141751048(a1: sub_140FE1560);
            sub_141750EA0(a1: &dword_141B608C0);
          }
        }
        v1342 = sub_1407E58C0(a1: &unk_141B60870, a2: 40);
        *(_QWORD *)v1342 = 0;
        *(_QWORD *)(v1342 + 8) = 0;
        *(_QWORD *)(v1342 + 16) = 0;
        *(_QWORD *)(v1342 + 24) = 0;
        *(_WORD *)(v1342 + 36) = -1;
        *(_BYTE *)(v1342 + 38) = -1;
        *(_DWORD *)(v1342 + 32) = 0;
        v1587[0] = v1595;
        if ( v1595 != nullptr )
          _InterlockedIncrement(v1595 + 2);
        v1343 = sub_14158B750(a1: v1342, a2: v1587, a3: v1341);
        v1344 = (void (__fastcall ***)(_QWORD, __int64))v1587[0];
        if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] + 8LL)) == 0 )
          (**v1344)(a1: v1344, a2: 1);
        LODWORD(v1599) = v1343;
        if ( (_BYTE)v1343 == 0 )
          break;
        v32 = a1[34];
        if ( v32 == a1[35] )
        {
          LODWORD(v1584) = v1161;
          v1345 = v32 - a1[33];
          v1346 = v1345 >> 3;
          v10 = (__int64)a1;
          v1347 = (unsigned __int64)(v1345 >> 3) >> 1;
          v1348 = 0x1FFFFFFFFFFFFFFFLL - v1347;
          v1349 = (v1345 >> 3) + v1347;
          v1598 = (v1345 >> 3) + 1;
          if ( v1349 <= v1598 )
            v1349 = v1346 + 1;
          if ( v1346 > v1348 )
            v1349 = 0x1FFFFFFFFFFFFFFFLL;
          v1350 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v1349);
          *(_QWORD *)(v1350 + v1345) = v1342;
          v1351 = *(_QWORD *)(v10 + 272);
          sub_141758A00(a1: v1350, a2: *(_QWORD *)(v10 + 264), a3: v32 - *(_QWORD *)(v10 + 264));
          if ( v1351 != v32 )
            sub_141758A00(a1: v1350 + v1345 + 8, a2: v32, a3: *(_QWORD *)(v10 + 272) - v32);
          v1352 = *(_QWORD *)(v10 + 264);
          v1341 = v1597;
          v1161 = v1584;
          if ( v1352 != 0 )
          {
            v1353 = *(_QWORD *)(v10 + 280) - v1352;
            if ( v1353 == -1 )
              v1353 = *(unsigned int *)(v1352 - *(unsigned int *)(qword_141ABD470 + 48));
            if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
              && (v1354 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v1354) >> 3 > v1353)
              && (v32 = *(_QWORD *)(v1354 + 8 * v1353)) != 0 )
            {
              MEMORY[0x1419475D8](a1: v32 + 32, a2: v1352 - *(unsigned int *)(v32 + 120));
              v1355 = *(_BYTE *)(v32 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v32 + 64)) != 0;
              v10 = (__int64)v1603;
              if ( !v1355 && *(_BYTE *)(v32 + 97) != 0 )
                sub_1412D33C0(a1: v32);
            }
            else
            {
              MEMORY[0x141948990](a1: v1352 - *(unsigned int *)(qword_141ABD470 + 48));
              v10 = (__int64)v1603;
            }
          }
          *(_QWORD *)(v10 + 264) = v1350;
          *(_QWORD *)(v10 + 272) = v1350 + 8 * v1598;
          *(_QWORD *)(v10 + 280) = v1350 + 8 * v1349;
          a1 = (_QWORD *)v10;
          LODWORD(v10) = (unsigned __int8)v1604;
        }
        else
        {
          *(_QWORD *)v32 = v1342;
          a1[34] += 8LL;
        }
        ++v1161;
      }
      while ( v1161 < (int)v1602 );
      goto LABEL_946;
    }
    v1162 = v1597;
    while ( 1 )
    {
      if ( dword_141B608C0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(a1: &dword_141B608C0);
        if ( dword_141B608C0 == -1 )
        {
          sub_1407E53D0(
            a1: (unsigned int)&unk_141B60870,
            a2: 1100150681,
            a3: 256,
            a4: 40,
            a5: 0,
            a6: 1,
            a7: 256,
            a8: 4096);
          sub_141751048(a1: sub_140FE1560);
          sub_141750EA0(a1: &dword_141B608C0);
        }
      }
      v32 = sub_1407E58C0(a1: &unk_141B60870, a2: 40);
      *(_QWORD *)v32 = 0;
      *(_QWORD *)(v32 + 8) = 0;
      *(_QWORD *)(v32 + 16) = 0;
      *(_QWORD *)(v32 + 24) = 0;
      *(_WORD *)(v32 + 36) = -1;
      *(_BYTE *)(v32 + 38) = -1;
      *(_DWORD *)(v32 + 32) = 0;
      v1587[0] = v1595;
      if ( v1595 != nullptr )
        _InterlockedIncrement(v1595 + 2);
      v1233 = sub_14158B750(a1: v32, a2: v1587, a3: v1162);
      v1234 = (void (__fastcall ***)(_QWORD, __int64))v1587[0];
      if ( v1587[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1587[0] + 8LL)) == 0 )
        (**v1234)(a1: v1234, a2: 1);
      if ( (_BYTE)v1233 == 0 )
        goto LABEL_945;
      LODWORD(v1598) = v1161;
      LODWORD(v1599) = v1233;
      v1235 = a1[33];
      v1236 = (__int64)a1;
      v1237 = (__int64 *)a1[34];
      v1238 = (__int64)v1237 - v1235;
      v1239 = (__int64 *)v1235;
      if ( (__int64)v1237 - v1235 > 0 )
      {
        v1240 = (unsigned __int64)v1238 >> 3;
        v1239 = (__int64 *)v1235;
        v1241 = (unsigned __int64)v1238 >> 3;
        do
        {
          v1241 = (unsigned __int64)v1241 >> 1;
          if ( *(_DWORD *)(v1239[v1241] + 32) < *(_DWORD *)(v32 + 32) )
          {
            v1239 += v1241 + 1;
            v1241 = v1240 + ~v1241;
          }
          v1240 = v1241;
        }
        while ( v1241 > 0 );
      }
      if ( v1239 == v1237 )
      {
        if ( v1237 == *(__int64 **)(v1236 + 280) )
        {
          v10 = v1236;
          v1262 = (unsigned __int64)(v1238 >> 3) >> 1;
          v1263 = 0x1FFFFFFFFFFFFFFFLL - v1262;
          v1264 = (v1238 >> 3) + v1262;
          v1584 = (v1238 >> 3) + 1;
          if ( v1264 <= v1584 )
            v1264 = (v1238 >> 3) + 1;
          if ( v1238 >> 3 > v1263 )
            v1264 = 0x1FFFFFFFFFFFFFFFLL;
          v1265 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v1264);
          *(_QWORD *)(v1265 + v1238) = v32;
          v1266 = *(__int64 **)(v10 + 272);
          sub_141758A00(a1: v1265, a2: *(_QWORD *)(v10 + 264), a3: (char *)v1237 - *(_QWORD *)(v10 + 264));
          if ( v1266 != v1237 )
            sub_141758A00(a1: v1265 + v1238 + 8, a2: v1237, a3: *(_QWORD *)(v10 + 272) - (_QWORD)v1237);
          v1267 = v1265;
          v1268 = *(_QWORD *)(v10 + 264);
          v1162 = v1597;
          if ( v1268 != 0 )
          {
            v1269 = *(_QWORD *)(v10 + 280) - v1268;
            if ( v1269 == -1 )
              v1269 = *(unsigned int *)(v1268 - *(unsigned int *)(qword_141ABD470 + 48));
            if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
              && (v1270 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v1270) >> 3 > v1269)
              && (v32 = *(_QWORD *)(v1270 + 8 * v1269)) != 0 )
            {
              MEMORY[0x1419475D8](a1: v32 + 32, a2: v1268 - *(unsigned int *)(v32 + 120));
              v1271 = *(_BYTE *)(v32 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v32 + 64)) != 0;
              v10 = (__int64)v1603;
              if ( !v1271 && *(_BYTE *)(v32 + 97) != 0 )
                sub_1412D33C0(a1: v32);
            }
            else
            {
              MEMORY[0x141948990](a1: v1268 - *(unsigned int *)(qword_141ABD470 + 48));
              v10 = (__int64)v1603;
            }
          }
          *(_QWORD *)(v10 + 264) = v1267;
          *(_QWORD *)(v10 + 272) = v1267 + 8 * v1584;
          *(_QWORD *)(v10 + 280) = v1267 + 8 * v1264;
          a1 = (_QWORD *)v10;
          LODWORD(v10) = (unsigned __int8)v1604;
          goto LABEL_2428;
        }
        *v1237 = v32;
        *(_QWORD *)(v1236 + 272) += 8LL;
        a1 = (_QWORD *)v1236;
      }
      else
      {
        v1242 = ((__int64)v1239 - v1235) >> 3;
        if ( *(_DWORD *)(*v1239 + 32) == *(_DWORD *)(v32 + 32) )
        {
          v1243 = v1238 >> 3;
          if ( v1243 > v1242 )
          {
            v1244 = *(__int64 **)(v1235 + 8 * v1242);
            if ( v1244 != nullptr )
            {
              sub_140E44A40(a1: v1244 + 3);
              v1245 = v1244[2];
              if ( v1245 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1245 - 4)) == 0 )
                sub_1412EC9A0(a1: v1245 - 4);
              v1246 = v1244[1];
              if ( v1246 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1246 - 4)) == 0 )
                sub_1412EC9A0(a1: v1246 - 4);
              v1247 = *v1244;
              if ( *v1244 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v1247 - 4)) == 0 )
                sub_1412EC9A0(a1: v1247 - 4);
              sub_140FE1400(a1: v1244);
              v1235 = v1603[33];
              v1237 = (__int64 *)v1603[34];
              v1243 = ((__int64)v1237 - v1235) >> 3;
            }
          }
          if ( v1243 <= v1242 )
          {
            v1248 = v1242 + 1;
            v1249 = v1242 + 1 - v1243;
            if ( v1242 + 1 < v1243 )
            {
              v1603[34] = v1235 + 8 * v1248;
            }
            else if ( v1242 + 1 > v1243 )
            {
              v1250 = v1603;
              v1251 = (v1603[35] - v1235) >> 3;
              if ( v1251 >= v1248 )
              {
                v1282 = &v1237[v1249];
                sub_141758A10(a1: v1237, a2: 0, a3: 8 * v1249);
                v1250[34] = v1282;
                v1235 = v1250[33];
              }
              else
              {
                v981 = v1248 >> 61;
                if ( v1248 >> 61 != 0 )
                  goto LABEL_3123;
                v1252 = v1251 + (v1251 >> 1);
                v1584 = v1242 + 1;
                if ( v1252 <= v1248 )
                  v1252 = v1242 + 1;
                if ( v1251 > 0x1FFFFFFFFFFFFFFFLL - (v1251 >> 1) )
                  v1252 = 0x1FFFFFFFFFFFFFFFLL;
                v1235 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v1252);
                sub_141758A10(a1: v1235 + 8 * v1243, a2: 0, a3: 8 * (v1242 + 1 - v1243));
                v1253 = v1603;
                sub_141758A00(a1: v1235, a2: v1603[33], a3: v1603[34] - v1603[33]);
                v1254 = v1253[33];
                if ( v1254 != 0 )
                {
                  v1255 = v1253[35] - v1254;
                  if ( v1255 == -1 )
                    v1255 = *(unsigned int *)(v1254 - *(unsigned int *)(qword_141ABD470 + 48));
                  if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                    && (v1256 = *(_QWORD *)(qword_141ABD470 + 24),
                        (*(_QWORD *)(qword_141ABD470 + 32) - v1256) >> 3 > v1255)
                    && (v1257 = *(_QWORD *)(v1256 + 8 * v1255)) != 0 )
                  {
                    MEMORY[0x1419475D8](a1: v1257 + 32, a2: v1254 - *(unsigned int *)(v1257 + 120));
                    v1258 = *(_BYTE *)(v1257 + 72) != 0
                         && _InterlockedDecrement((volatile signed __int32 *)(v1257 + 64)) != 0;
                    v1253 = v1603;
                    if ( !v1258 && *(_BYTE *)(v1257 + 97) != 0 )
                      sub_1412D33C0(a1: v1257);
                  }
                  else
                  {
                    MEMORY[0x141948990](a1: v1254 - *(unsigned int *)(qword_141ABD470 + 48));
                    v1253 = v1603;
                  }
                }
                v1253[33] = v1235;
                v1253[34] = v1235 + 8 * v1584;
                v1253[35] = v1235 + 8 * v1252;
              }
              LODWORD(v10) = (unsigned __int8)v1604;
            }
          }
          *(_QWORD *)(v1235 + 8 * v1242) = v32;
          a1 = v1603;
        }
        else
        {
          v1259 = (__int64 *)(v1235 + 8 * v1242);
          v10 = (__int64)v1603;
          if ( v1237 == (__int64 *)v1603[35] )
          {
            v1272 = v1238 >> 3;
            v1273 = v1272 + 1;
            v1274 = v1272 + (v1272 >> 1);
            if ( v1274 <= v1272 + 1 )
              v1274 = v1272 + 1;
            if ( v1272 > 0x1FFFFFFFFFFFFFFFLL - (v1272 >> 1) )
              v1274 = 0x1FFFFFFFFFFFFFFFLL;
            v1275 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v1274);
            *(_QWORD *)(v1275 + 8 * v1242) = v32;
            v1276 = *(__int64 **)(v10 + 272);
            sub_141758A00(a1: v1275, a2: *(_QWORD *)(v10 + 264), a3: (char *)v1259 - *(_QWORD *)(v10 + 264));
            if ( v1276 != v1259 )
              sub_141758A00(a1: v1275 + 8 * v1242 + 8, a2: v1259, a3: *(_QWORD *)(v10 + 272) - (_QWORD)v1259);
            v1277 = *(_QWORD *)(v10 + 264);
            LODWORD(v32) = (unsigned __int8)v1604;
            if ( v1277 != 0 )
            {
              v1278 = *(_QWORD *)(v10 + 280) - v1277;
              if ( v1278 == -1 )
                v1278 = *(unsigned int *)(v1277 - *(unsigned int *)(qword_141ABD470 + 48));
              if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                && (v1279 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v1279) >> 3 > v1278)
                && (v1280 = *(_QWORD *)(v1279 + 8 * v1278)) != 0 )
              {
                MEMORY[0x1419475D8](a1: v1280 + 32, a2: v1277 - *(unsigned int *)(v1280 + 120));
                v1281 = *(_BYTE *)(v1280 + 72) != 0
                     && _InterlockedDecrement((volatile signed __int32 *)(v1280 + 64)) != 0;
                v10 = (__int64)v1603;
                if ( !v1281 && *(_BYTE *)(v1280 + 97) != 0 )
                  sub_1412D33C0(a1: v1280);
              }
              else
              {
                MEMORY[0x141948990](a1: v1277 - *(unsigned int *)(qword_141ABD470 + 48));
                v10 = (__int64)v1603;
              }
            }
            *(_QWORD *)(v10 + 264) = v1275;
            *(_QWORD *)(v10 + 272) = v1275 + 8 * v1273;
            *(_QWORD *)(v10 + 280) = v1275 + 8 * v1274;
            a1 = (_QWORD *)v10;
            LODWORD(v10) = v32;
          }
          else
          {
            if ( v1237 == v1259 )
            {
              *v1237 = v32;
              a1 = v1603;
              v1603[34] += 8LL;
            }
            else
            {
              *v1237 = *(v1237 - 1);
              v1260 = v1603;
              v1603[34] += 8LL;
              v1261 = (char *)(v1237 - 1) - (char *)v1259;
              a1 = v1260;
              sub_141758A00(a1: v1259 + 1, a2: v1235 + 8 * v1242, a3: v1261);
              *v1259 = v32;
            }
            LODWORD(v10) = (unsigned __int8)v1604;
          }
        }
      }
      v1162 = v1597;
LABEL_2428:
      v1161 = v1598 + 1;
      if ( (int)v1598 + 1 >= (int)v1602 )
        goto LABEL_946;
    }
  }
  return (unsigned int)v32;
}
