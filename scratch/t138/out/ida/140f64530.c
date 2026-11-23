bool __fastcall sub_140F64530(_QWORD *a1, __int64 a2, unsigned __int8 a3, _BYTE *a4, char a5, __int64 a6, __int64 a7)
{
  _QWORD *v7; // r13
  __int64 v8; // rdi
  __int64 v9; // rax
  int v11; // ebx
  __int64 *v12; // rax
  __int64 v13; // rsi
  __int64 v14; // r14
  __int64 v15; // rax
  _QWORD *v16; // rsi
  _QWORD *v17; // r14
  __int64 *v18; // rcx
  __int64 v19; // rax
  __int64 i; // rcx
  __int64 v21; // rsi
  volatile signed __int32 *v22; // rcx
  volatile signed __int32 *v23; // rcx
  unsigned __int16 v24; // dx
  volatile signed __int32 *v25; // rsi
  __int64 v26; // r9
  char v27; // si
  __int64 v28; // rdi
  unsigned int v29; // r13d
  unsigned int v30; // eax
  double v31; // xmm6_8
  char v32; // al
  char v33; // cl
  __int64 **v34; // rcx
  __int64 *v35; // rax
  __int64 *v36; // r10
  __int64 v37; // rbx
  __int64 v38; // rdx
  __int64 v39; // rdi
  unsigned __int64 v40; // rdi
  _QWORD *v41; // rcx
  __int64 *v42; // rbx
  unsigned __int64 v43; // rbx
  __int64 *v44; // rcx
  __int64 v45; // r9
  __int64 v46; // rbx
  _QWORD *v47; // rax
  _QWORD *v48; // rbx
  _QWORD *v49; // r15
  unsigned int (*v50)(void); // r13
  __int64 v51; // rdi
  char v52; // r12
  __int64 v53; // rax
  _QWORD *v54; // r14
  __int64 *v55; // rax
  __int64 v56; // rcx
  __int64 v57; // rax
  __int64 v58; // rcx
  __int64 v59; // rax
  __int64 v60; // rsi
  unsigned int v61; // eax
  __int64 v62; // rax
  __int64 v63; // rsi
  void (__fastcall ***v64)(_QWORD, __int64); // rcx
  _QWORD *v65; // r14
  void (__fastcall ***v66)(_QWORD, __int64); // rcx
  void (__fastcall ***v67)(_QWORD, __int64); // rcx
  void (__fastcall ***v68)(_QWORD, __int64); // rcx
  __int64 v69; // rax
  __int64 v70; // rcx
  __int64 *v71; // rdx
  __int64 v72; // rax
  _QWORD *v73; // r14
  __int64 *v74; // rax
  __int64 v75; // rcx
  __int64 v76; // rax
  __int64 v77; // rcx
  __int64 v78; // rax
  __int64 v79; // rsi
  unsigned int v80; // eax
  __int64 v81; // rax
  __int64 v82; // rsi
  void (__fastcall ***v83)(_QWORD, __int64); // rcx
  _QWORD *v84; // r14
  void (__fastcall ***v85)(_QWORD, __int64); // rcx
  void (__fastcall ***v86)(_QWORD, __int64); // rcx
  void (__fastcall ***v87)(_QWORD, __int64); // rcx
  __int64 v88; // rax
  __int64 v89; // rsi
  __int64 v90; // rdi
  __int64 v91; // rax
  __int64 v92; // r8
  __int64 v93; // rax
  __int64 v94; // r8
  _QWORD *v95; // r12
  int v96; // eax
  char v97; // bl
  __int64 v98; // r9
  void (__fastcall ***v99)(_QWORD, __int64); // rcx
  int v100; // ebx
  __int64 v101; // rax
  __int64 v102; // rax
  __int16 v103; // r8
  __int16 v104; // cx
  int v105; // eax
  __int64 v106; // rdx
  __int64 *v107; // rax
  unsigned __int8 v108; // al
  int v109; // ebx
  _QWORD *v110; // rbx
  char v111; // al
  char v112; // cl
  unsigned __int64 v113; // rax
  __int64 v114; // rdx
  unsigned __int64 v115; // r15
  __int64 v116; // r14
  unsigned int v117; // edi
  __int64 j; // rbx
  __int64 v119; // rax
  __int64 v120; // r12
  _QWORD *v121; // r15
  void (__fastcall ***v122)(_QWORD, __int64); // rcx
  __int64 v123; // rcx
  __int64 *v124; // r13
  __int64 v125; // rbx
  __int64 v126; // rdi
  __int64 v127; // r15
  __int64 v128; // r14
  __int64 v129; // r12
  __int64 v130; // rbx
  void (__fastcall ***v131)(_QWORD, __int64); // rcx
  int v132; // edi
  volatile signed __int32 *v133; // rbx
  __int64 v134; // r12
  _QWORD *v135; // rbx
  int v136; // r8d
  __int64 v137; // r9
  unsigned __int64 v138; // rax
  _QWORD *v139; // rdx
  _QWORD *v140; // r12
  __int64 v141; // r14
  __int64 **v142; // rax
  __int64 *v143; // rdi
  __int64 *v144; // r15
  __int64 v145; // rsi
  unsigned int v146; // ebx
  char v147; // al
  char v148; // cl
  void (__fastcall ***v149)(_QWORD, __int64); // rcx
  volatile signed __int32 *v150; // rsi
  __int64 v151; // r9
  char v152; // si
  char v153; // si
  unsigned int v154; // edi
  volatile signed __int32 *v155; // rbx
  __int64 v156; // r12
  _QWORD *v157; // rbx
  int v158; // r8d
  __int64 v159; // r9
  unsigned __int64 v160; // rax
  _QWORD *v161; // rdx
  volatile signed __int32 *v162; // rcx
  void (__fastcall ***v163)(_QWORD, __int64); // rcx
  volatile signed __int32 *v164; // rcx
  volatile signed __int32 *v165; // rcx
  __int64 v166; // rcx
  _QWORD *v167; // r12
  __int64 v168; // r14
  __int64 **v169; // rax
  __int64 *v170; // rdi
  __int64 *v171; // r15
  __int64 v172; // rsi
  unsigned int v173; // ebx
  char v174; // al
  char v175; // cl
  void (__fastcall ***v176)(_QWORD, __int64); // rcx
  void (__fastcall ***v177)(_QWORD, __int64); // rcx
  __int64 v178; // rbx
  _QWORD *v179; // r12
  unsigned __int64 v180; // r15
  __int64 v181; // rdi
  unsigned int v182; // ebx
  __int64 v183; // r13
  __int64 k; // rsi
  __int64 v185; // rax
  __int64 v186; // r14
  _QWORD *v187; // r12
  __int64 v188; // rcx
  __int64 v189; // rcx
  _QWORD *v190; // r13
  __int64 *v191; // r12
  __int64 v192; // rdi
  __int64 v193; // r15
  __int64 v194; // rcx
  __int64 v195; // r14
  __int64 v196; // rsi
  __int64 v197; // rbx
  __int64 v198; // rcx
  __int64 v199; // rbx
  __int64 v200; // r12
  unsigned int v201; // ebx
  __int64 v202; // rdi
  unsigned __int64 v203; // r14
  __int64 v204; // r13
  __int64 v205; // rax
  volatile signed __int32 *v206; // r15
  _QWORD *v207; // rdi
  __int64 v208; // rcx
  _QWORD *v209; // rsi
  _QWORD **v210; // rdx
  __int64 v211; // rcx
  unsigned __int64 v212; // rdi
  unsigned __int64 v213; // r8
  unsigned __int64 v214; // rax
  __int64 v215; // rdi
  unsigned __int64 v216; // rdx
  __int64 v217; // r15
  __int64 v218; // rdx
  __int64 v219; // r8
  _QWORD *v220; // rcx
  __int64 v221; // rdi
  unsigned __int64 v222; // rcx
  __int64 v223; // r8
  __int64 v224; // rsi
  bool v225; // al
  __int64 *v226; // r12
  __int64 v227; // rdi
  __int64 v228; // r14
  __int64 v229; // rcx
  __int64 v230; // r15
  __int64 v231; // rsi
  __int64 v232; // rbx
  __int64 v233; // rcx
  __int64 v234; // rbx
  __int64 v235; // rax
  unsigned __int64 v236; // rdi
  __int64 v237; // rax
  __int64 v238; // rsi
  __int64 v239; // rax
  __int64 v240; // rax
  __int64 *v241; // rax
  __int64 *v242; // rdx
  __int64 *v243; // rcx
  __int64 *v244; // rdi
  unsigned __int8 v245; // si
  unsigned int v246; // ebx
  __int64 v247; // r14
  __int64 v248; // rax
  __int64 v249; // rax
  char v250; // bl
  __int64 v251; // rax
  __int64 v252; // rax
  __int64 v253; // rax
  __int64 v254; // rax
  __int64 v255; // rax
  unsigned __int64 v256; // rax
  __int64 v257; // rsi
  __int64 m; // rdi
  _QWORD *v259; // rdx
  int v260; // eax
  __int64 v261; // rdx
  __int64 v262; // rax
  __int64 v263; // rcx
  __int64 *v264; // rdi
  _QWORD *v265; // r14
  _QWORD *v266; // rdi
  _QWORD *v267; // rsi
  _QWORD *v268; // rbx
  __int64 v269; // rax
  volatile signed __int32 **v270; // rsi
  volatile signed __int32 **v271; // rdi
  volatile signed __int32 **v272; // rdi
  __int64 v273; // rbx
  unsigned int ***v274; // rax
  unsigned int **v275; // rbx
  unsigned int **v276; // r13
  volatile signed __int32 *v277; // r12
  unsigned int *v278; // rdi
  __int64 v279; // rax
  __int64 v280; // r9
  unsigned int v281; // ecx
  unsigned int v282; // edx
  __int64 v283; // rsi
  __int64 *v284; // rax
  __int64 *v285; // r14
  __int64 v286; // rcx
  __int64 v287; // rax
  volatile signed __int32 *v288; // rcx
  volatile signed __int32 *v289; // r12
  _QWORD *v290; // r14
  _QWORD *v291; // rcx
  _QWORD *v292; // rsi
  unsigned __int64 v293; // rdi
  __int64 *v295; // rbx
  __int64 v296; // rax
  __int64 v297; // rcx
  _QWORD *v298; // rax
  _QWORD *v299; // rdi
  __int64 v300; // rbx
  char v301; // al
  __int64 v302; // rax
  unsigned __int64 v303; // rax
  __int64 v304; // rdi
  __int64 n; // rbx
  __int64 v306; // rsi
  __int64 v307; // rax
  __int16 v308; // cx
  __int64 v309; // rax
  __int16 v310; // cx
  __int64 v311; // rax
  __int16 v312; // cx
  int v313; // r14d
  _QWORD *v314; // r13
  char *v315; // r10
  char ***v316; // rax
  __int64 *v317; // r15
  char *v318; // rcx
  char *v319; // rsi
  unsigned __int64 v320; // rbx
  int v321; // r13d
  __int16 v322; // cx
  __int64 v323; // rdi
  int v324; // r12d
  __int16 v325; // ax
  char *v326; // r14
  __int64 v327; // r10
  unsigned __int64 v328; // rax
  unsigned __int64 v329; // rdx
  unsigned __int64 v330; // rax
  unsigned __int64 v331; // rsi
  __int64 v332; // rax
  __int64 v333; // rcx
  __int64 v334; // rsi
  __int64 v335; // rsi
  __int64 v336; // rcx
  unsigned __int64 v337; // r14
  unsigned __int64 v338; // r9
  unsigned __int64 v339; // r8
  unsigned __int64 v340; // rdi
  __int64 v341; // r14
  char *v342; // rdi
  unsigned __int64 v343; // rax
  __int64 v344; // rdi
  __int64 v345; // rdi
  unsigned __int64 v346; // rcx
  __int64 v347; // r8
  __int64 v348; // r14
  char *v349; // rax
  _QWORD *v350; // rdi
  char *v351; // rbx
  __int64 v352; // rbx
  __int64 v353; // rbx
  unsigned __int64 v354; // rbx
  unsigned __int64 v355; // rax
  __int64 v356; // rcx
  unsigned __int64 v357; // rbx
  __int64 v358; // rdi
  __int64 v359; // r15
  __int64 v360; // rdi
  __int64 v361; // rbx
  _QWORD *v362; // r13
  __int64 *v363; // r12
  __int64 v364; // rsi
  _QWORD *v365; // rcx
  __int64 v366; // rax
  char *v367; // rdi
  __int64 *v368; // rsi
  __int64 v369; // rcx
  unsigned __int64 v370; // rbx
  __int64 v371; // rcx
  __int64 v372; // rsi
  bool v373; // al
  __int64 v374; // rsi
  __int64 v375; // rcx
  volatile signed __int32 *v376; // rax
  unsigned int v377; // ecx
  void (__fastcall ***v378)(_QWORD, __int64); // rcx
  volatile signed __int32 *v379; // rcx
  volatile signed __int32 *v380; // rdi
  __int64 v381; // rsi
  char v382; // bl
  __int64 v383; // rcx
  __int64 v384; // rsi
  int v385; // r9d
  void (__fastcall ***v386)(_QWORD, __int64); // rcx
  _QWORD *v387; // r14
  volatile signed __int32 *v388; // rcx
  volatile signed __int32 *v389; // rcx
  void (__fastcall ***v390)(_QWORD, __int64); // rcx
  unsigned __int64 v391; // rcx
  __int64 v392; // rbx
  __int64 v393; // rsi
  bool v394; // al
  unsigned __int64 v395; // rcx
  __int64 v396; // rbx
  __int64 v397; // rsi
  bool v398; // al
  unsigned __int64 v399; // rcx
  __int64 v400; // rbx
  __int64 v401; // rsi
  bool v402; // al
  unsigned __int64 v403; // rcx
  __int64 v404; // rbx
  __int64 v405; // rsi
  bool v406; // al
  __int64 v407; // rcx
  __int64 v408; // rdx
  __int64 *v409; // rdi
  __int64 v410; // rcx
  __int64 v411; // rdx
  __int64 v412; // rcx
  char v413; // dl
  _BYTE *v414; // rdi
  _BYTE *v415; // rcx
  __int64 v416; // r12
  __int64 v417; // rdi
  __int64 v418; // r15
  unsigned __int64 v419; // rax
  unsigned __int64 v420; // r13
  __int64 v421; // rax
  __int64 v422; // r12
  __int64 v423; // rbx
  unsigned __int64 v424; // rcx
  __int64 v425; // rdi
  __int64 v426; // rdi
  bool v427; // al
  __int64 *v428; // rax
  __int64 v429; // rsi
  __int64 v430; // r14
  __int64 v431; // rcx
  __int64 v432; // rdx
  __int64 *v433; // rdi
  __int64 v434; // rcx
  __int64 v435; // rdx
  __int64 v436; // rcx
  char v437; // dl
  _BYTE *v438; // rdi
  _BYTE *v439; // rcx
  __int64 v440; // r12
  __int64 v441; // rdi
  __int64 v442; // r15
  unsigned __int64 v443; // rax
  unsigned __int64 v444; // r13
  __int64 v445; // rax
  __int64 v446; // r12
  __int64 v447; // rbx
  unsigned __int64 v448; // rcx
  __int64 v449; // rdi
  __int64 v450; // rdi
  bool v451; // al
  __int64 v452; // rsi
  int v453; // edi
  __int64 v454; // rsi
  int v455; // edi
  __int64 v457; // rbx
  __int64 v458; // r15
  __int64 v459; // rdi
  __int64 v460; // r12
  unsigned __int64 v461; // rcx
  __int64 v462; // r8
  __int64 v463; // r14
  bool v464; // al
  unsigned __int64 v465; // rbx
  __int64 v466; // r15
  __int64 v467; // rdi
  __int64 v468; // r12
  unsigned __int64 v469; // rcx
  __int64 v470; // r8
  __int64 v471; // r14
  bool v472; // al
  __int64 v473; // r15
  __int64 v474; // r14
  __int64 v475; // rbx
  __int64 v476; // rsi
  __int64 *v477; // rcx
  __int64 v478; // rax
  __int64 v479; // r14
  unsigned __int64 v480; // rbx
  _QWORD **v481; // rdx
  __int64 *v482; // rcx
  unsigned __int64 v483; // r14
  unsigned __int64 v484; // rsi
  __int64 v485; // rcx
  __int64 v486; // rax
  __int64 v487; // rbx
  __int64 v488; // r9
  char v489; // bl
  bool v490; // r15
  unsigned __int64 v491; // rdx
  int v492; // edi
  int v493; // edi
  unsigned __int64 v494; // rcx
  __int64 v495; // rcx
  volatile signed __int32 *v496; // rsi
  volatile signed __int32 *v497; // rcx
  signed __int32 v498; // et0
  __int64 v499; // rbx
  __int64 v500; // r15
  __int64 v501; // rbx
  int v502; // [rsp+20h] [rbp-60h]
  int v503; // [rsp+20h] [rbp-60h]
  int v504; // [rsp+28h] [rbp-58h]
  int v505; // [rsp+28h] [rbp-58h]
  int v506; // [rsp+30h] [rbp-50h]
  char ***v507; // [rsp+60h] [rbp-20h]
  char ***v508; // [rsp+68h] [rbp-18h]
  int v509; // [rsp+70h] [rbp-10h]
  __int64 v510; // [rsp+78h] [rbp-8h] BYREF
  _QWORD **v511; // [rsp+80h] [rbp+0h]
  unsigned __int64 v512; // [rsp+88h] [rbp+8h]
  __int64 v513; // [rsp+90h] [rbp+10h] BYREF
  char *v514; // [rsp+98h] [rbp+18h]
  __int64 v515; // [rsp+A0h] [rbp+20h]
  _QWORD *v516; // [rsp+A8h] [rbp+28h]
  __int64 v517; // [rsp+B0h] [rbp+30h] BYREF
  volatile signed __int32 *v518; // [rsp+B8h] [rbp+38h] BYREF
  volatile signed __int32 *v519; // [rsp+C0h] [rbp+40h] BYREF
  unsigned __int64 v520; // [rsp+C8h] [rbp+48h]
  _QWORD *v521; // [rsp+D0h] [rbp+50h]
  __int64 v522; // [rsp+D8h] [rbp+58h]
  __int64 v523; // [rsp+E0h] [rbp+60h] BYREF
  char v524; // [rsp+E8h] [rbp+68h]
  _QWORD v525[2]; // [rsp+F0h] [rbp+70h] BYREF

  v525[1] = -2;
  v7 = a1;
  v8 = a7;
  v9 = a1[13];
  if ( a7 == 0 )
    v8 = a1[13];
  v11 = a2;
  v521 = a1;
  switch ( HIDWORD(qword_141B5E548) )
  {
    case 0:
      sub_140F685A0(a1: a2, a2: a1 + 249);
      v18 = (__int64 *)v7[191];
      v19 = *v18;
      for ( i = v18[1]; v19 != i; v19 += 8 )
        *(_QWORD *)(*(_QWORD *)v19 + 24LL) |= 0x400000uLL;
      if ( (qword_141B5E548 & 2) != 0 )
      {
        sub_140F237E0(a1: v8);
        HIDWORD(qword_141B5E548) = 4;
        return true;
      }
      v523 = 0x80100004E554C4CLL;
      sub_14080D0E0(a1: &v519, a2: 0x1418E2C24LL);
      v21 = sub_1412EC810(a1: 264, a2: 9);
      *(_QWORD *)v21 = 0x900000000LL;
      strcpy((char *)(v21 + 8), "people_db");
      _InterlockedIncrement((volatile signed __int32 *)v21);
      v518 = nullptr;
      _InterlockedIncrement((volatile signed __int32 *)v21);
      v518 = (volatile signed __int32 *)(v21 + 4);
      sub_1407D0F70(
        a1: (unsigned int)&v523,
        a2: (unsigned int)v525,
        a3: v11,
        a4: (unsigned int)&v518,
        a5: (__int64)&v519,
        a6: 0,
        a7: 0,
        a8: 0);
      v22 = v518;
      if ( v518 != nullptr && _InterlockedDecrement(v518 - 1) == 0 )
        sub_1412EC9A0(a1: v22 - 1);
      if ( _InterlockedDecrement((volatile signed __int32 *)v21) == 0 )
        sub_1412EC9A0(a1: v21);
      v23 = (volatile signed __int32 *)v525[0];
      if ( v525[0] == 0 )
        return false;
      v24 = *((_WORD *)v7 + 709);
      if ( WORD2(v523) != v24 && v24 < 0xDB2u )
      {
        if ( _InterlockedDecrement((volatile signed __int32 *)(v525[0] + 8LL)) == 0 )
          (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v23)(a1: v23, a2: 1);
        return false;
      }
      *((_WORD *)v7 + 708) = WORD2(v523);
      v518 = v23;
      _InterlockedIncrement(v23 + 2);
      sub_1407CC0B0(a1: &v519, a2: &v518);
      v162 = v518;
      if ( v518 != nullptr && _InterlockedDecrement(v518 + 2) == 0 )
        (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v162)(a1: v162, a2: 1);
      v518 = v519;
      if ( v519 != nullptr )
        _InterlockedIncrement(v519 + 2);
      sub_140803850(a1: &v510, a2: &v518, a3: 0x10000);
      v163 = (void (__fastcall ***)(_QWORD, __int64))qword_141B5E550;
      if ( qword_141B5E550 == v510 )
      {
        if ( qword_141B5E550 != 0 && _InterlockedDecrement((volatile signed __int32 *)(qword_141B5E550 + 8)) == 0 )
          (**v163)(a1: v163, a2: 1);
      }
      else
      {
        if ( qword_141B5E550 != 0 && _InterlockedDecrement((volatile signed __int32 *)(qword_141B5E550 + 8)) == 0 )
          (**v163)(a1: v163, a2: 1);
        qword_141B5E550 = v510;
        v510 = 0;
      }
      v164 = v518;
      if ( v518 != nullptr && _InterlockedDecrement(v518 + 2) == 0 )
        (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v164)(a1: v164, a2: 1);
      HIDWORD(qword_141B5E548) = 1;
      v165 = v519;
      if ( v519 != nullptr && _InterlockedDecrement(v519 + 2) == 0 )
        (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v165)(a1: v165, a2: 1);
      v166 = v525[0];
      goto LABEL_697;
    case 1:
    case 2:
      *a4 = 0;
      if ( v8 == 0 )
        v8 = a1[13];
      v520 = v8;
      if ( HIDWORD(qword_141B5E548) != 2 )
      {
        if ( HIDWORD(qword_141B5E548) != 1 )
          return true;
        if ( qword_141B5E558 != qword_141B5E560 )
          qword_141B5E560 = qword_141B5E558;
        *(_BYTE *)(v8 + 90) = 0;
        sub_1408B6C90(a1: a1[199], a2: a1[200], a3: (__int64)(a1[200] - a1[199]) >> 2);
        if ( (qword_141B5E548 & 1) == 0 )
        {
          v12 = *(__int64 **)(v7[106] + 128LL);
          v13 = *v12;
          v14 = v12[1];
          if ( *v12 != v14 )
          {
            while ( 1 )
            {
              v407 = *(_QWORD *)(*(_QWORD *)v13 + 32LL);
              if ( v407 == 0 )
                goto LABEL_717;
              v408 = *(_QWORD *)(v407 + 48);
              v409 = (__int64 *)(v408 + 368);
              if ( *(_BYTE *)(v407 + 47) == 0 )
                v409 = (__int64 *)(v408 + 216);
              v410 = *v409;
              if ( *v409 != 0 )
              {
                if ( *(_BYTE *)(v408 + 185) == 0 || (v411 = *(_QWORD *)(v410 + 272)) == 0 )
                  v411 = *(_QWORD *)(v410 + 264);
                if ( (_BYTE)word_141B60320 != 0 )
                {
                  v412 = *(_QWORD *)(*(_QWORD *)(v411 + 368) + 288LL);
                  if ( v412 != 0 )
                  {
                    v413 = *(_BYTE *)(v411 + 185);
                    if ( v413 == 0 )
                      break;
                    v414 = *(_BYTE **)(v412 + 624);
                    if ( v414 != nullptr )
                      goto LABEL_731;
                  }
                }
              }
LABEL_717:
              v13 += 8;
              if ( v13 == v14 )
                goto LABEL_758;
            }
            v414 = *(_BYTE **)(v412 + 624);
LABEL_731:
            v415 = (_BYTE *)(v412 + 88);
            if ( v413 != 0 )
              v415 = v414;
            if ( v415 != nullptr && *(_BYTE *)(*(_QWORD *)v415 + 68LL) != 0 && (v415[522] & 0xFD) == 0 )
            {
              v416 = *(_QWORD *)(*(_QWORD *)v13 + 24LL);
              if ( (int)v416 >= 0 )
              {
                v417 = qword_141B5E560;
                if ( qword_141B5E560 == qword_141B5E568 )
                {
                  v418 = qword_141B5E560 - qword_141B5E558;
                  v419 = (qword_141B5E560 - qword_141B5E558) >> 2;
                  v420 = v419 + (v419 >> 1);
                  v522 = v419 + 1;
                  if ( v420 <= v419 + 1 )
                    v420 = v419 + 1;
                  if ( v419 > 0x3FFFFFFFFFFFFFFFLL - (v419 >> 1) )
                    v420 = 0x3FFFFFFFFFFFFFFFLL;
                  v421 = sub_1407E4490(a1: qword_141ABD470, a2: 4 * v420);
                  *(_DWORD *)(v421 + v418) = v416;
                  v422 = v421;
                  v423 = qword_141B5E560;
                  sub_141758A00(a1: v421, a2: qword_141B5E558, a3: v417 - qword_141B5E558);
                  if ( v423 != v417 )
                    sub_141758A00(a1: v422 + v418 + 4, a2: v417, a3: qword_141B5E560 - v417);
                  if ( qword_141B5E558 != 0 )
                  {
                    v424 = qword_141B5E568 - qword_141B5E558;
                    if ( qword_141B5E568 - qword_141B5E558 == -1 )
                      v424 = *(unsigned int *)(qword_141B5E558 - *(unsigned int *)(qword_141ABD470 + 48));
                    if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                      && (v425 = *(_QWORD *)(qword_141ABD470 + 24),
                          (*(_QWORD *)(qword_141ABD470 + 32) - v425) >> 3 > v424)
                      && (v426 = *(_QWORD *)(v425 + 8 * v424)) != 0 )
                    {
                      MEMORY[0x1419475D8](a1: v426 + 32, a2: qword_141B5E558 - *(unsigned int *)(v426 + 120));
                      v427 = *(_BYTE *)(v426 + 72) != 0
                          && _InterlockedDecrement((volatile signed __int32 *)(v426 + 64)) != 0;
                      if ( !v427 && *(_BYTE *)(v426 + 97) != 0 )
                        sub_1412D33C0(a1: v426);
                    }
                    else
                    {
                      MEMORY[0x141948990](a1: qword_141B5E558 - *(unsigned int *)(qword_141ABD470 + 48));
                    }
                  }
                  qword_141B5E558 = v422;
                  qword_141B5E560 = v422 + 4 * v522;
                  qword_141B5E568 = v422 + 4 * v420;
                  v7 = v521;
                }
                else
                {
                  *(_DWORD *)qword_141B5E560 = v416;
                  qword_141B5E560 += 4;
                }
              }
            }
            goto LABEL_717;
          }
LABEL_758:
          v428 = *(__int64 **)(v7[109] + 128LL);
          v429 = *v428;
          v430 = v428[1];
          if ( *v428 != v430 )
          {
            while ( 1 )
            {
              v431 = *(_QWORD *)(*(_QWORD *)v429 + 80LL);
              if ( v431 == 0 )
                goto LABEL_761;
              v432 = *(_QWORD *)(v431 + 48);
              v433 = (__int64 *)(v432 + 368);
              if ( *(_BYTE *)(v431 + 47) == 0 )
                v433 = (__int64 *)(v432 + 216);
              v434 = *v433;
              if ( *v433 != 0 )
              {
                if ( *(_BYTE *)(v432 + 185) == 0 || (v435 = *(_QWORD *)(v434 + 272)) == 0 )
                  v435 = *(_QWORD *)(v434 + 264);
                if ( (_BYTE)word_141B60320 != 0 )
                {
                  v436 = *(_QWORD *)(*(_QWORD *)(v435 + 368) + 288LL);
                  if ( v436 != 0 )
                  {
                    v437 = *(_BYTE *)(v435 + 185);
                    if ( v437 == 0 )
                      break;
                    v438 = *(_BYTE **)(v436 + 624);
                    if ( v438 != nullptr )
                      goto LABEL_775;
                  }
                }
              }
LABEL_761:
              v429 += 8;
              if ( v429 == v430 )
                goto LABEL_802;
            }
            v438 = *(_BYTE **)(v436 + 624);
LABEL_775:
            v439 = (_BYTE *)(v436 + 88);
            if ( v437 != 0 )
              v439 = v438;
            if ( v439 != nullptr && *(_BYTE *)(*(_QWORD *)v439 + 68LL) != 0 && (v439[522] & 0xFD) == 0 )
            {
              v440 = *(_QWORD *)(*(_QWORD *)v429 + 72LL);
              if ( (int)v440 >= 0 )
              {
                v441 = qword_141B5E560;
                if ( qword_141B5E560 == qword_141B5E568 )
                {
                  v442 = qword_141B5E560 - qword_141B5E558;
                  v443 = (qword_141B5E560 - qword_141B5E558) >> 2;
                  v444 = v443 + (v443 >> 1);
                  v522 = v443 + 1;
                  if ( v444 <= v443 + 1 )
                    v444 = v443 + 1;
                  if ( v443 > 0x3FFFFFFFFFFFFFFFLL - (v443 >> 1) )
                    v444 = 0x3FFFFFFFFFFFFFFFLL;
                  v445 = sub_1407E4490(a1: qword_141ABD470, a2: 4 * v444);
                  *(_DWORD *)(v445 + v442) = v440;
                  v446 = v445;
                  v447 = qword_141B5E560;
                  sub_141758A00(a1: v445, a2: qword_141B5E558, a3: v441 - qword_141B5E558);
                  if ( v447 != v441 )
                    sub_141758A00(a1: v446 + v442 + 4, a2: v441, a3: qword_141B5E560 - v441);
                  if ( qword_141B5E558 != 0 )
                  {
                    v448 = qword_141B5E568 - qword_141B5E558;
                    if ( qword_141B5E568 - qword_141B5E558 == -1 )
                      v448 = *(unsigned int *)(qword_141B5E558 - *(unsigned int *)(qword_141ABD470 + 48));
                    if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                      && (v449 = *(_QWORD *)(qword_141ABD470 + 24),
                          (*(_QWORD *)(qword_141ABD470 + 32) - v449) >> 3 > v448)
                      && (v450 = *(_QWORD *)(v449 + 8 * v448)) != 0 )
                    {
                      MEMORY[0x1419475D8](a1: v450 + 32, a2: qword_141B5E558 - *(unsigned int *)(v450 + 120));
                      v451 = *(_BYTE *)(v450 + 72) != 0
                          && _InterlockedDecrement((volatile signed __int32 *)(v450 + 64)) != 0;
                      if ( !v451 && *(_BYTE *)(v450 + 97) != 0 )
                        sub_1412D33C0(a1: v450);
                    }
                    else
                    {
                      MEMORY[0x141948990](a1: qword_141B5E558 - *(unsigned int *)(qword_141ABD470 + 48));
                    }
                  }
                  qword_141B5E558 = v446;
                  qword_141B5E560 = v446 + 4 * v522;
                  qword_141B5E568 = v446 + 4 * v444;
                  v7 = v521;
                }
                else
                {
                  *(_DWORD *)qword_141B5E560 = v440;
                  qword_141B5E560 += 4;
                }
              }
            }
            goto LABEL_761;
          }
LABEL_802:
          sub_1408B6C90(a1: qword_141B5E558, a2: qword_141B5E560, a3: (qword_141B5E560 - qword_141B5E558) >> 2);
        }
        LOWORD(v525[0]) = 0;
        if ( *((unsigned __int16 *)v7 + 708) >= 0xDC3u )
        {
          v452 = qword_141B5E550;
          if ( qword_141B5E550 != 0 )
            _InterlockedIncrement((volatile signed __int32 *)(qword_141B5E550 + 8));
          (*(void (__fastcall **)(__int64, _QWORD *, __int64))(*(_QWORD *)v452 + 40LL))(a1: v452, a2: v525, a3: 2);
          v453 = *(_DWORD *)(v452 + 16);
          if ( _InterlockedDecrement((volatile signed __int32 *)(v452 + 8)) == 0 )
            (**(void (__fastcall ***)(__int64, __int64))v452)(a1: v452, a2: 1);
          if ( v453 != 0 )
            return false;
        }
        v454 = qword_141B5E550;
        if ( qword_141B5E550 != 0 )
          _InterlockedIncrement((volatile signed __int32 *)(qword_141B5E550 + 8));
        (*(void (__fastcall **)(__int64, __int64 *, __int64))(*(_QWORD *)v454 + 40LL))(
          a1: v454,
          a2: &qword_141B5E5C8,
          a3: 4);
        v455 = *(_DWORD *)(v454 + 16);
        if ( _InterlockedDecrement((volatile signed __int32 *)(v454 + 8)) == 0 )
          (**(void (__fastcall ***)(__int64, __int64))v454)(a1: v454, a2: 1);
        if ( v455 != 0 )
          return false;
        LOBYTE(qword_141B5E5C0) = 1;
        v457 = (unsigned int)qword_141B5E5C8;
        HIDWORD(qword_141B5E5C0) = (unsigned int)qword_141B5E5C8 / 0x1E - 1;
        v458 = qword_141B5E570;
        if ( (qword_141B5E580 - qword_141B5E570) >> 1 < (unsigned __int64)(unsigned int)qword_141B5E5C8 )
        {
          v459 = qword_141B5E578;
          v460 = sub_1407E4490(a1: qword_141ABD470, a2: 2LL * (unsigned int)qword_141B5E5C8);
          sub_141758A00(a1: v460, a2: qword_141B5E570, a3: qword_141B5E578 - qword_141B5E570);
          if ( qword_141B5E570 != 0 )
          {
            v461 = qword_141B5E580 - qword_141B5E570;
            if ( qword_141B5E580 - qword_141B5E570 == -1 )
              v461 = *(unsigned int *)(qword_141B5E570 - *(unsigned int *)(qword_141ABD470 + 48));
            if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
              && (v462 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v462) >> 3 > v461)
              && (v463 = *(_QWORD *)(v462 + 8 * v461)) != 0 )
            {
              MEMORY[0x1419475D8](a1: v463 + 32, a2: qword_141B5E570 - *(unsigned int *)(v463 + 120));
              v464 = *(_BYTE *)(v463 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v463 + 64)) != 0;
              if ( !v464 && *(_BYTE *)(v463 + 97) != 0 )
                sub_1412D33C0(a1: v463);
            }
            else
            {
              MEMORY[0x141948990](a1: qword_141B5E570 - *(unsigned int *)(qword_141ABD470 + 48));
            }
          }
          qword_141B5E570 = v460;
          qword_141B5E578 = v460 + v459 - v458;
          qword_141B5E580 = v460 + 2 * v457;
          v457 = (unsigned int)qword_141B5E5C8;
        }
        v465 = (unsigned __int64)(v457 + 31) >> 5;
        v466 = qword_141B5E588;
        if ( (qword_141B5E598 - qword_141B5E588) >> 2 < v465 )
        {
          v467 = qword_141B5E590;
          v468 = sub_1407E4490(a1: qword_141ABD470, a2: 4 * v465);
          sub_141758A00(a1: v468, a2: qword_141B5E588, a3: qword_141B5E590 - qword_141B5E588);
          if ( qword_141B5E588 != 0 )
          {
            v469 = qword_141B5E598 - qword_141B5E588;
            if ( qword_141B5E598 - qword_141B5E588 == -1 )
              v469 = *(unsigned int *)(qword_141B5E588 - *(unsigned int *)(qword_141ABD470 + 48));
            if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
              && (v470 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v470) >> 3 > v469)
              && (v471 = *(_QWORD *)(v470 + 8 * v469)) != 0 )
            {
              MEMORY[0x1419475D8](a1: v471 + 32, a2: qword_141B5E588 - *(unsigned int *)(v471 + 120));
              v472 = *(_BYTE *)(v471 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v471 + 64)) != 0;
              if ( !v472 && *(_BYTE *)(v471 + 97) != 0 )
                sub_1412D33C0(a1: v471);
            }
            else
            {
              MEMORY[0x141948990](a1: qword_141B5E588 - *(unsigned int *)(qword_141ABD470 + 48));
            }
          }
          qword_141B5E588 = v468;
          qword_141B5E590 = v468 + v467 - v466;
          qword_141B5E598 = v468 + 4 * v465;
        }
        if ( (unsigned __int8)sub_1400015B0() != 0 )
        {
          v473 = (unsigned int)qword_141B5E5C8;
          v474 = qword_141B5E5A8;
          if ( (qword_141B5E5B8 - qword_141B5E5A8) >> 2 < (unsigned __int64)(unsigned int)qword_141B5E5C8 )
          {
            v475 = qword_141B5E5B0;
            v476 = sub_1407E4490(a1: qword_141ABD470, a2: 4LL * (unsigned int)qword_141B5E5C8);
            sub_141758A00(a1: v476, a2: qword_141B5E5A8, a3: qword_141B5E5B0 - qword_141B5E5A8);
            if ( qword_141B5E5A8 != 0 )
              sub_1407E4890(a1: qword_141ABD470, a2: qword_141B5E5A8, a3: qword_141B5E5B8 - qword_141B5E5A8);
            qword_141B5E5A8 = v476;
            qword_141B5E5B0 = v476 + v475 - v474;
            qword_141B5E5B8 = v476 + 4 * v473;
          }
        }
        v477 = *(__int64 **)(v520 + 128);
        v478 = *v477;
        v479 = v477[1];
        if ( v479 == *v477 )
        {
          v481 = *(_QWORD ***)(v7[13] + 128LL);
          v478 = v477[1];
          v480 = v520;
          if ( v481[1] != *v481 )
          {
            v480 = v520;
            if ( (*(__int64 (__fastcall **)(_QWORD))(*(_QWORD *)**v481 + 1816LL))(a1: **v481) != 0 )
              v480 = v7[13];
            v482 = *(__int64 **)(v480 + 128);
            v478 = *v482;
            v479 = v482[1];
          }
        }
        else
        {
          v480 = v520;
        }
        v522 = v480;
        if ( (_DWORD)qword_141B5E5C8 == 0 )
        {
LABEL_868:
          HIDWORD(qword_141B5E548) = 2;
          HIDWORD(qword_141B5E5C8) = 0;
          return true;
        }
        v483 = (v479 - v478) >> 3;
        v484 = 0;
        while ( 1 )
        {
          if ( v484 < v483 && (v485 = *(_QWORD *)(**(_QWORD **)(v522 + 128) + 8 * v484)) != 0 )
          {
            v486 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v485 + 1816LL))(a1: v485);
            LOWORD(v519) = -2;
            LODWORD(v523) = 0;
            if ( v486 != 0 )
            {
              v487 = v486;
              if ( (*(_BYTE *)(v486 + 103) & 7) != 0 )
              {
                if ( (unsigned __int8)sub_140087040() != 0 )
                {
                  LOWORD(v519) = *(_WORD *)(v487 + 86);
                }
                else
                {
                  LOWORD(v519) = -1;
                  LODWORD(v523) = *(_DWORD *)(v487 + 72);
                }
              }
              sub_140F6A100(a1: &v519, a2: v484);
              sub_14094B000(a1: &qword_141B5E5A8, a2: &v523, a3: v484);
              v490 = (*(_BYTE *)(v487 + 102) & 2) != 0;
              v489 = 1;
              if ( qword_141B5E5A0 > v484 )
                goto LABEL_860;
LABEL_859:
              sub_1409ECDB0(a1: &qword_141B5E588, a2: v484 + 1);
              goto LABEL_860;
            }
          }
          else
          {
            LODWORD(v523) = 0;
          }
          sub_140087040();
          LOWORD(v519) = -1;
          sub_140F6A100(a1: &v519, a2: v484);
          sub_14094B000(a1: &qword_141B5E5A8, a2: &v523, a3: v484);
          v489 = 0;
          v490 = false;
          if ( qword_141B5E5A0 <= v484 )
            goto LABEL_859;
LABEL_860:
          v491 = v484 >> 5;
          v492 = 1 << v484;
          if ( v490 )
            v493 = *(_DWORD *)(qword_141B5E588 + 4 * v491) | v492;
          else
            v493 = *(_DWORD *)(qword_141B5E588 + 4 * v491) & ~v492;
          v494 = v520;
          *(_DWORD *)(qword_141B5E588 + 4 * v491) = v493;
          if ( v489 != 0 )
          {
            LOBYTE(v488) = 1;
            sub_140F6A2E0(a1: v494, a2: 0, a3: (unsigned int)v484, a4: v488);
          }
          if ( ++v484 >= (unsigned int)qword_141B5E5C8 )
            goto LABEL_868;
        }
      }
      v28 = qword_141B5E550;
      if ( qword_141B5E550 != 0 )
        _InterlockedIncrement((volatile signed __int32 *)(qword_141B5E550 + 8));
      v29 = qword_141B5E5C8;
      *((_BYTE *)v521 + 1451) = 1;
      v30 = HIDWORD(qword_141B5E5C8);
      if ( HIDWORD(qword_141B5E5C8) < v29 )
      {
        v31 = MEMORY[0x14186AAC0];
        do
        {
          if ( a6 != 0 && v30 == HIDWORD(qword_141B5E5C0) )
          {
            LOBYTE(qword_141B5E5C0) = qword_141B5E5C0 + 1;
            HIDWORD(qword_141B5E5C0) = (char)qword_141B5E5C0 * v29 / 0x1E - 1;
            v153 = 1;
            v109 = 1;
            if ( v28 == 0 )
              return ((unsigned __int8)v153 | (v109 == 0)) != 0;
LABEL_241:
            if ( _InterlockedDecrement((volatile signed __int32 *)(v28 + 8)) == 0 )
              (**(void (__fastcall ***)(__int64, __int64))v28)(a1: v28, a2: 1);
            return ((unsigned __int8)v153 | (v109 == 0)) != 0;
          }
          (*(void (__fastcall **)(__int64, _QWORD *, __int64))(*(_QWORD *)v28 + 40LL))(a1: v28, a2: v525, a3: 4);
          if ( *(_DWORD *)(v28 + 16) != 0 )
            goto LABEL_239;
          if ( SLODWORD(v525[0]) < 0 )
            goto LABEL_239;
          if ( LODWORD(v525[0]) >= v29 )
            goto LABEL_239;
          (*(void (__fastcall **)(__int64, volatile signed __int32 **, __int64))(*(_QWORD *)v28 + 40LL))(
            a1: v28,
            a2: &v519,
            a3: 1);
          if ( *(_DWORD *)(v28 + 16) != 0 )
            goto LABEL_239;
          v93 = sub_1410992C0(a1: (unsigned __int8)v519);
          if ( v93 == 0 )
            goto LABEL_239;
          v95 = (_QWORD *)v93;
          v96 = v525[0];
          v523 = v28;
          _InterlockedIncrement((volatile signed __int32 *)(v28 + 8));
          LOBYTE(v506) = 1;
          LOBYTE(v94) = 1;
          v97 = (*(__int64 (__fastcall **)(_QWORD *, __int64 *, __int64, _QWORD *, int, int, int, unsigned __int64))(*v95 + 152LL))(
                  a1: v95,
                  a2: &v523,
                  a3: v94,
                  a4: v521,
                  a5: 1,
                  a6: v96,
                  a7: v506,
                  a8: v520);
          v99 = (void (__fastcall ***)(_QWORD, __int64))v523;
          if ( v523 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v523 + 8)) == 0 )
            (**v99)(a1: v99, a2: 1);
          if ( v97 == 0 )
          {
LABEL_239:
            v109 = 1;
            goto LABEL_240;
          }
          v100 = *(__int16 *)(qword_141B5E570 + 2LL * SLODWORD(v525[0]));
          if ( v100 != -2 )
          {
            if ( (unsigned __int8)sub_1400015B0() != 0 )
            {
              v101 = (*(__int64 (__fastcall **)(_QWORD *))(*v95 + 1720LL))(a1: v95);
              if ( v101 != 0 )
                *(_DWORD *)(v101 + 464) = *(_DWORD *)(qword_141B5E5A8 + 4LL * SLODWORD(v525[0]));
            }
            if ( (v100 & 0x8000u) == 0 )
            {
              v102 = (*(__int64 (__fastcall **)(_QWORD *))(*v95 + 1720LL))(a1: v95);
              if ( v102 != 0 )
              {
                v103 = *(_WORD *)(v102 + 512);
                v98 = (unsigned int)(__int16)v100;
                v104 = 200;
                if ( (int)v98 < 200 )
                  v104 = v100;
                *(_WORD *)(v102 + 512) = v104;
                if ( *(_BYTE *)(v102 + 605) > (unsigned __int8)v104 )
                  LOBYTE(v104) = *(_BYTE *)(v102 + 605);
                *(_BYTE *)(v102 + 605) = v104;
                if ( (unsigned __int16)v100 >= 0x10u
                  && ((double)(int)v98 > (double)v103 * v31 || v103 + 5 < v100)
                  && *(__int16 *)(v102 + 508) < (int)(unsigned __int16)(v100 - 15) )
                {
                  *(_DWORD *)(v102 + 506) = 0;
                  *(_WORD *)(v102 + 510) = 0;
                }
              }
            }
          }
          v92 = SLODWORD(v525[0]);
          v105 = *(_DWORD *)(qword_141B5E588 + 4 * ((unsigned __int64)SLODWORD(v525[0]) >> 5));
          v106 = -67108865;
          v95[3] = v95[3] & 0xFFFFFFFFFBFFFFFFuLL | ((unsigned __int64)_bittest(&v105, v525[0]) << 26);
          if ( (_WORD)v100 == 0xFFFE )
          {
            if ( (qword_141B5E498 & 0x100000000LL) == 0 )
            {
LABEL_173:
              if ( a3 == 0 )
                goto LABEL_140;
              goto LABEL_139;
            }
            v107 = &qword_141B5E480;
            while ( 1 )
            {
              v107 = (__int64 *)v107[2];
              if ( v107 == nullptr || *v107 == 0 )
                break;
              if ( (*((_BYTE *)v107 + 28) & 1) == 0 )
                goto LABEL_173;
            }
          }
          LOBYTE(v503) = 16;
          LOBYTE(v106) = 1;
          LOBYTE(v98) = 1;
          v108 = (*(__int64 (__fastcall **)(_QWORD *, __int64, _QWORD *, __int64, int))(*v95 + 160LL))(
                   a1: v95,
                   a2: v106,
                   a3: v521,
                   a4: v98,
                   a5: v503);
          if ( (a3 & v108) == 1 && (_WORD)v100 == 0xFFFE )
          {
            v92 = LODWORD(v525[0]);
LABEL_139:
            LOBYTE(v98) = 1;
            sub_140F6A2E0(a1: v520, a2: 0, a3: v92, a4: v98);
            goto LABEL_140;
          }
          v109 = 1;
          if ( v108 != 0 )
            v109 = 11;
          if ( (a3 & v108) != 0 )
            v109 = 0;
          if ( v109 != 11 && v109 != 0 )
            goto LABEL_240;
LABEL_140:
          v30 = HIDWORD(qword_141B5E5C8) + 1;
          HIDWORD(qword_141B5E5C8) = v30;
        }
        while ( v30 < v29 );
      }
      v110 = v521;
      *((_BYTE *)v521 + 1451) = 0;
      v111 = *(_BYTE *)(v110[12] + 89LL) | 2;
      if ( *(_BYTE *)(*v110 + 89LL) == 0 )
        v111 = *(_BYTE *)(v110[12] + 89LL);
      v112 = v111 | 4;
      if ( *(_BYTE *)(v110[13] + 89LL) == 0 )
        v112 = v111;
      v113 = v520;
      *(_BYTE *)(v520 + 90) = v112;
      *(_BYTE *)(v113 + 89) = 1;
      *((_BYTE *)v110 + 1721) = 0;
      HIDWORD(qword_141B5E548) = 3;
      v109 = 0;
LABEL_240:
      v153 = 0;
      if ( v28 != 0 )
        goto LABEL_241;
      return ((unsigned __int8)v153 | (v109 == 0)) != 0;
    case 3:
      v25 = (volatile signed __int32 *)qword_141B5E550;
      if ( qword_141B5E550 != 0 )
        _InterlockedIncrement((volatile signed __int32 *)(qword_141B5E550 + 8));
      v523 = (__int64)v25;
      (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *, __int64))(*(_QWORD *)v25 + 40LL))(
        a1: v25,
        a2: v525,
        a3: 4);
      if ( *((_DWORD *)v25 + 4) != 0 )
        goto LABEL_35;
      if ( SLODWORD(v525[0]) <= 0 )
        goto LABEL_221;
      v132 = 0;
      LOBYTE(v26) = 1;
      sub_140F6B4D0(a1: v521[103], a2: 0, a3: (unsigned int)(LODWORD(v525[0]) - 1), a4: v26);
      if ( SLODWORD(v525[0]) <= 0 )
        goto LABEL_221;
      do
      {
        v133 = (volatile signed __int32 *)v523;
        (*(void (__fastcall **)(__int64, volatile signed __int32 **, __int64))(*(_QWORD *)v523 + 40LL))(
          a1: v523,
          a2: &v519,
          a3: 1);
        if ( *((_DWORD *)v133 + 4) != 0 )
        {
LABEL_35:
          v27 = 0;
          goto LABEL_231;
        }
        if ( dword_141ABF448 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                         + 4LL) )
        {
          sub_141750E08(a1: &dword_141ABF448);
          if ( dword_141ABF448 == -1 )
          {
            sub_1407E53D0(
              a1: (unsigned int)&unk_141ABF3F8,
              a2: 1100122405,
              a3: 128,
              a4: 88,
              a5: 0,
              a6: 0,
              a7: 128,
              a8: 4096);
            sub_141751048(a1: sub_140E41970);
            sub_141750EA0(a1: &dword_141ABF448);
          }
        }
        v134 = sub_1407E58C0(a1: &unk_141ABF3F8, a2: 88);
        *(_QWORD *)(v134 + 8) = -1;
        *(_DWORD *)(v134 + 16) = 0;
        *(_QWORD *)v134 = 0x1418822B8LL;
        *(_QWORD *)(v134 + 48) = -1;
        *(_QWORD *)(v134 + 56) = -1;
        *(_QWORD *)(v134 + 64) = 0x76C0001076C0001LL;
        *(_DWORD *)(v134 + 72) = 124518401;
        *(_BYTE *)(v134 + 87) = 0;
        *(_BYTE *)(v134 + 84) = 0;
        *(_QWORD *)(v134 + 24) = 0;
        *(_QWORD *)(v134 + 32) = 0;
        *(_QWORD *)(v134 + 76) = 0x76C076CFFFFFFFFLL;
        *(_WORD *)(v134 + 85) = 0;
        *(_QWORD *)(v134 + 40) = 0;
        v135 = v521;
        LOBYTE(v136) = 1;
        if ( (unsigned __int8)sub_141438DB0(
                                a1: v134,
                                a2: (unsigned int)&v523,
                                a3: v136,
                                a4: (_DWORD)v521,
                                a5: 14,
                                a6: v132,
                                a7: 1,
                                a8: v521[103]) == 0 )
        {
          sub_140E41800(a1: v134);
          v27 = 0;
          goto LABEL_231;
        }
        v138 = *(int *)(v134 + 24);
        v139 = *(_QWORD **)(v135[13] + 128LL);
        if ( v138 >= (__int64)(v139[1] - *v139) >> 3 || *(_QWORD *)(*v139 + 8 * v138) == 0 )
        {
          LOBYTE(v137) = 1;
          sub_140F6B4D0(a1: v521[103], a2: 0, a3: (unsigned int)v132, a4: v137);
        }
        ++v132;
      }
      while ( v132 < SLODWORD(v525[0]) );
LABEL_221:
      v140 = v521;
      v141 = v521[103];
      v142 = *(__int64 ***)(v141 + 128);
      v143 = *v142;
      v144 = v142[1];
      while ( v143 != v144 )
      {
        v145 = *v143;
        if ( *v143 != 0 )
        {
          v146 = *(unsigned __int8 *)(v141 + 90);
          sub_140F80250(a1: v140, a2: v145 + 24, a3: *(unsigned __int8 *)(v141 + 90), a4: 0);
          sub_140F7FF40(a1: v140, a2: v145 + 32, a3: v146, a4: 0);
        }
        ++v143;
      }
      v147 = *(_BYTE *)(v140[12] + 89LL) | 2;
      if ( *(_BYTE *)(*v140 + 89LL) == 0 )
        v147 = *(_BYTE *)(v140[12] + 89LL);
      v148 = v147 | 4;
      if ( *(_BYTE *)(v140[13] + 89LL) == 0 )
        v148 = v147;
      *(_BYTE *)(v141 + 90) = v148;
      v27 = 1;
LABEL_231:
      v149 = (void (__fastcall ***)(_QWORD, __int64))v523;
      if ( v523 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v523 + 8)) == 0 )
        (**v149)(a1: v149, a2: 1);
      if ( v27 == 0 )
        return false;
      v150 = (volatile signed __int32 *)qword_141B5E550;
      if ( qword_141B5E550 != 0 )
        _InterlockedIncrement((volatile signed __int32 *)(qword_141B5E550 + 8));
      v523 = (__int64)v150;
      (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *, __int64))(*(_QWORD *)v150 + 40LL))(
        a1: v150,
        a2: v525,
        a3: 4);
      if ( *((_DWORD *)v150 + 4) != 0 )
        goto LABEL_238;
      if ( SLODWORD(v525[0]) <= 0
        || (v154 = 0,
            LOBYTE(v151) = 1,
            sub_140F6B800(a1: v521[104], a2: 0, a3: (unsigned int)(LODWORD(v525[0]) - 1), a4: v151),
            SLODWORD(v525[0]) <= 0) )
      {
LABEL_275:
        v167 = v521;
        v168 = v521[104];
        v169 = *(__int64 ***)(v168 + 128);
        v170 = *v169;
        v171 = v169[1];
        while ( v170 != v171 )
        {
          v172 = *v170;
          if ( *v170 != 0 )
          {
            v173 = *(unsigned __int8 *)(v168 + 90);
            sub_140F80250(a1: v167, a2: v172 + 24, a3: *(unsigned __int8 *)(v168 + 90), a4: 0);
            sub_140F7FF40(a1: v167, a2: v172 + 32, a3: v173, a4: 0);
          }
          ++v170;
        }
        v174 = *(_BYTE *)(v167[12] + 89LL) | 2;
        if ( *(_BYTE *)(*v167 + 89LL) == 0 )
          v174 = *(_BYTE *)(v167[12] + 89LL);
        v175 = v174 | 4;
        if ( *(_BYTE *)(v167[13] + 89LL) == 0 )
          v175 = v174;
        *(_BYTE *)(v168 + 90) = v175;
        v152 = 1;
      }
      else
      {
        while ( 1 )
        {
          v155 = (volatile signed __int32 *)v523;
          (*(void (__fastcall **)(__int64, volatile signed __int32 **, __int64))(*(_QWORD *)v523 + 40LL))(
            a1: v523,
            a2: &v519,
            a3: 1);
          if ( *((_DWORD *)v155 + 4) != 0 )
            break;
          if ( dword_141B5F2D0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer
                                             + (unsigned int)TlsIndex)
                                           + 4LL) )
          {
            sub_141750E08(a1: &dword_141B5F2D0);
            if ( dword_141B5F2D0 == -1 )
            {
              sub_1407E53D0(
                a1: (unsigned int)&unk_141B5F280,
                a2: 1100122401,
                a3: 128,
                a4: 64,
                a5: 0,
                a6: 0,
                a7: 128,
                a8: 4096);
              sub_141751048(a1: sub_140FB3BD0);
              sub_141750EA0(a1: &dword_141B5F2D0);
            }
          }
          v156 = sub_1407E58C0(a1: &unk_141B5F280, a2: 64);
          *(_QWORD *)(v156 + 8) = -1;
          *(_DWORD *)(v156 + 16) = 0;
          *(_QWORD *)v156 = 0x141882418LL;
          *(_QWORD *)(v156 + 40) = 0x76C0001076C0001LL;
          *(_QWORD *)(v156 + 48) = -4170448895LL;
          *(_BYTE *)(v156 + 58) = 0;
          *(_WORD *)(v156 + 59) = 256;
          *(_QWORD *)(v156 + 24) = 0;
          *(_QWORD *)(v156 + 32) = 0;
          *(_WORD *)(v156 + 56) = 11;
          v157 = v521;
          LOBYTE(v158) = 1;
          if ( (unsigned __int8)sub_141454370(
                                  a1: v156,
                                  a2: (unsigned int)&v523,
                                  a3: v158,
                                  a4: (_DWORD)v521,
                                  a5: 44,
                                  a6: v154,
                                  a7: 1,
                                  a8: v521[104]) == 0 )
          {
            sub_140F6BAB0(a1: v156);
            v152 = 0;
            goto LABEL_285;
          }
          v160 = *(int *)(v156 + 24);
          v161 = *(_QWORD **)(v157[13] + 128LL);
          if ( v160 >= (__int64)(v161[1] - *v161) >> 3 || *(_QWORD *)(*v161 + 8 * v160) == 0 )
          {
            LOBYTE(v159) = 1;
            sub_140F6B800(a1: v521[104], a2: 0, a3: v154, a4: v159);
          }
          if ( (int)++v154 >= SLODWORD(v525[0]) )
            goto LABEL_275;
        }
LABEL_238:
        v152 = 0;
      }
LABEL_285:
      v176 = (void (__fastcall ***)(_QWORD, __int64))v523;
      if ( v523 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v523 + 8)) == 0 )
        (**v176)(a1: v176, a2: 1);
      if ( v152 == 0 )
        return false;
      v177 = (void (__fastcall ***)(_QWORD, __int64))qword_141B5E550;
      if ( qword_141B5E550 != 0 )
      {
        if ( _InterlockedDecrement((volatile signed __int32 *)(qword_141B5E550 + 8)) == 0 )
          (**v177)(a1: v177, a2: 1);
        qword_141B5E550 = 0;
      }
      HIDWORD(qword_141B5E548) = 4;
      return true;
    case 4:
      v509 = a2;
      v520 = v8;
      LOBYTE(v514) = a3;
      v522 = (__int64)a4;
      if ( v8 == v9 )
      {
        *(_BYTE *)(v9 + 89) = 1;
        LOBYTE(a2) = 32;
        sub_140F3C890(a1, a2);
        LOBYTE(v114) = 32;
        sub_140F3E690(a1: v7, a2: v114);
      }
      else
      {
        a1[24] = v8;
        *(_BYTE *)(v8 + 90) = *(_BYTE *)(v8 + 90) & 0xDB | 0x20;
        v15 = *(_QWORD *)(v8 + 128);
        v16 = *(_QWORD **)v15;
        v17 = *(_QWORD **)(v15 + 8);
        while ( v16 != v17 )
        {
          if ( *v16 != 0 )
          {
            LOBYTE(v502) = *(_BYTE *)(v8 + 90);
            LOBYTE(a2) = 1;
            LOBYTE(a4) = 1;
            (*(void (__fastcall **)(_QWORD, __int64, _QWORD *, _BYTE *, int))(*(_QWORD *)*v16 + 160LL))(
              a1: *v16,
              a2,
              a3: v7,
              a4,
              a5: v502);
          }
          ++v16;
        }
        v32 = *(_BYTE *)(v7[12] + 89LL) | 2;
        if ( *(_BYTE *)(*v7 + 89LL) == 0 )
          v32 = *(_BYTE *)(v7[12] + 89LL);
        v33 = v32 | 4;
        if ( *(_BYTE *)(v7[13] + 89LL) == 0 )
          v33 = v32;
        *(_BYTE *)(v8 + 90) = v33;
        v34 = *(__int64 ***)(v7[106] + 128LL);
        v35 = *v34;
        v36 = v34[1];
        if ( *v34 != v36 )
        {
          v37 = qword_141B5FE68;
          while ( 1 )
          {
            v38 = *v35;
            v39 = *(_QWORD *)(*v35 + 24);
            if ( v37 != 0 )
              break;
            if ( v39 == 0 )
            {
              v43 = *(unsigned int *)(v38 + 80);
              if ( (v43 & 0x80000000) == 0LL )
              {
                v44 = *(__int64 **)(qword_141B5FE10 + 128);
                if ( (v44[1] - *v44) >> 3 > v43 )
                {
                  if ( (_BYTE)word_141B60320 == 0
                    && (v45 = *(_QWORD *)(qword_141B5FE10 + 96), (*(_QWORD *)(qword_141B5FE10 + 104) - v45) >> 3 > v43)
                    || (v45 = *v44, v44[1] != *v44) )
                  {
                    v42 = (__int64 *)(v45 + 8 * v43);
                    goto LABEL_60;
                  }
                  v46 = 0;
LABEL_61:
                  *(_QWORD *)(v38 + 24) = v46;
                  v37 = qword_141B5FE68;
                  goto LABEL_48;
                }
              }
            }
            v37 = 0;
LABEL_48:
            if ( ++v35 == v36 )
              goto LABEL_63;
          }
          if ( v39 != 0 )
            goto LABEL_48;
          v40 = *(unsigned int *)(v38 + 80);
          if ( (v40 & 0x80000000) != 0LL )
            goto LABEL_48;
          v41 = *(_QWORD **)(v37 + 128);
          if ( (__int64)(v41[1] - *v41) >> 3 <= v40 )
            goto LABEL_48;
          v42 = (__int64 *)(*v41 + 8 * v40);
LABEL_60:
          v46 = *v42;
          goto LABEL_61;
        }
LABEL_63:
        v7[24] = 0;
        if ( (qword_141B5E548 & 0x80u) == 0LL )
        {
          v47 = *(_QWORD **)(v520 + 128);
          v48 = (_QWORD *)*v47;
          v49 = (_QWORD *)v47[1];
          if ( (_QWORD *)*v47 != v49 )
          {
            v50 = (unsigned int (*)(void))MEMORY[0x141947498];
            do
            {
              v51 = *v48;
              if ( *v48 == 0 || (*(__int64 (__fastcall **)(_QWORD))(*(_QWORD *)v51 + 1816LL))(a1: *v48) != 0 )
                goto LABEL_67;
              v52 = qword_141B5E548;
              v53 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v51 + 672LL))(a1: v51);
              if ( v53 != 0 )
              {
                v54 = (_QWORD *)v53;
                if ( (v52 & 0x20) != 0
                  && (v55 = *(__int64 **)(v53 + 24)) != (__int64 *)v54[4]
                  && (v56 = *v55, *v55 != 0)
                  && (*(_BYTE *)(v56 + 40) == 0 ? (v57 = *(_QWORD *)(v56 + 128)) : (v57 = sub_1411A41D0()), v57 != 0) )
                {
                  v58 = v57 + *(int *)(*(_QWORD *)(v57 + 8) + 4LL) + 8;
                  if ( (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v58 + 1760LL))(a1: v58) == 0 && (v52 & 0x40) == 0 )
                  {
LABEL_80:
                    v59 = (*(__int64 (__fastcall **)(__int64, _QWORD *, _QWORD))(*(_QWORD *)v51 + 1024LL))(
                            a1: v51,
                            a2: v54,
                            a3: 0);
                    if ( v59 != 0 )
                    {
                      v60 = v59;
                      v61 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v59 + 120LL))(a1: v59);
                      (*(void (__fastcall **)(_QWORD *, __int64, _QWORD, _QWORD, _QWORD))(*v54 + 512LL))(
                        a1: v54,
                        a2: v51,
                        a3: *(unsigned __int16 *)(v60 + 30),
                        a4: v61,
                        a5: 0);
                    }
                    goto LABEL_97;
                  }
                }
                else if ( (v52 & 0x40) == 0 )
                {
                  goto LABEL_80;
                }
                v62 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v51 + 1704LL))(a1: v51);
                if ( v62 != 0 )
                {
                  v63 = v62;
                  v64 = *(void (__fastcall ****)(_QWORD, __int64))(v62 + 160);
                  if ( v64 != nullptr )
                    (**v64)(a1: v64, a2: 1);
                  *(_QWORD *)(v63 + 160) = 0;
                  v65 = *(_QWORD **)(v63 + 168);
                  if ( v65 != nullptr )
                  {
                    if ( *v65 != 0 )
                      (**(void (__fastcall ***)(_QWORD, __int64))*v65)(a1: *v65, a2: 1);
                    v66 = (void (__fastcall ***)(_QWORD, __int64))v65[1];
                    if ( v66 != nullptr )
                      (**v66)(a1: v66, a2: 1);
                    v67 = (void (__fastcall ***)(_QWORD, __int64))v65[2];
                    if ( v67 != nullptr )
                      (**v67)(a1: v67, a2: 1);
                    v68 = (void (__fastcall ***)(_QWORD, __int64))v65[3];
                    if ( v68 != nullptr )
                      (**v68)(a1: v68, a2: 1);
                    sub_140DF11C0(a1: v65);
                  }
                  *(_QWORD *)(v63 + 168) = 0;
                }
              }
LABEL_97:
              v69 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v51 + 1096LL))(a1: v51);
              if ( v69 != 0 )
              {
                v70 = *(_QWORD *)(v69 + 48);
                v71 = (__int64 *)(v70 + 368);
                if ( *(_BYTE *)(v69 + 47) == 0 )
                  v71 = (__int64 *)(v70 + 216);
                v72 = *v71;
                if ( *v71 != 0
                  && (*(_BYTE *)(v70 + 185) != 0 && (v73 = *(_QWORD **)(v72 + 272)) != nullptr
                   || (v73 = *(_QWORD **)(v72 + 264)) != nullptr) )
                {
                  if ( (v52 & 0x20) != 0
                    && (v74 = (__int64 *)v73[3]) != (__int64 *)v73[4]
                    && (v75 = *v74, *v74 != 0)
                    && (*(_BYTE *)(v75 + 40) == 0 ? (v76 = *(_QWORD *)(v75 + 128)) : (v76 = sub_1411A41D0()), v76 != 0) )
                  {
                    v77 = v76 + *(int *)(*(_QWORD *)(v76 + 8) + 4LL) + 8;
                    if ( (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v77 + 1760LL))(a1: v77) == 0
                      && (v52 & 0x40) == 0 )
                    {
LABEL_113:
                      v78 = (*(__int64 (__fastcall **)(__int64, _QWORD *, _QWORD))(*(_QWORD *)v51 + 1024LL))(
                              a1: v51,
                              a2: v73,
                              a3: 0);
                      if ( v78 != 0 )
                      {
                        v79 = v78;
                        v80 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v78 + 120LL))(a1: v78);
                        (*(void (__fastcall **)(_QWORD *, __int64, _QWORD, _QWORD, _QWORD))(*v73 + 512LL))(
                          a1: v73,
                          a2: v51,
                          a3: *(unsigned __int16 *)(v79 + 30),
                          a4: v80,
                          a5: 0);
                      }
                      goto LABEL_130;
                    }
                  }
                  else if ( (v52 & 0x40) == 0 )
                  {
                    goto LABEL_113;
                  }
                  v81 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v51 + 1704LL))(a1: v51);
                  if ( v81 != 0 )
                  {
                    v82 = v81;
                    v83 = *(void (__fastcall ****)(_QWORD, __int64))(v81 + 160);
                    if ( v83 != nullptr )
                      (**v83)(a1: v83, a2: 1);
                    *(_QWORD *)(v82 + 160) = 0;
                    v84 = *(_QWORD **)(v82 + 168);
                    if ( v84 != nullptr )
                    {
                      if ( *v84 != 0 )
                        (**(void (__fastcall ***)(_QWORD, __int64))*v84)(a1: *v84, a2: 1);
                      v85 = (void (__fastcall ***)(_QWORD, __int64))v84[1];
                      if ( v85 != nullptr )
                        (**v85)(a1: v85, a2: 1);
                      v86 = (void (__fastcall ***)(_QWORD, __int64))v84[2];
                      if ( v86 != nullptr )
                        (**v86)(a1: v86, a2: 1);
                      v87 = (void (__fastcall ***)(_QWORD, __int64))v84[3];
                      if ( v87 != nullptr )
                        (**v87)(a1: v87, a2: 1);
                      sub_140DF11C0(a1: v84);
                    }
                    *(_QWORD *)(v82 + 168) = 0;
                  }
                }
              }
LABEL_130:
              v88 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v51 + 1720LL))(a1: v51);
              if ( v88 == 0 )
                goto LABEL_67;
              v89 = v88;
              if ( byte_141B595A8 != 0 )
              {
                v90 = qword_141B595B0;
                if ( v90 == v50() )
                  goto LABEL_135;
              }
              else if ( qword_141B5A658 == v50() )
              {
LABEL_135:
                v91 = *(_QWORD *)(v89 + 280);
                if ( v91 != 0 )
                {
                  *(_QWORD *)v91 = -1;
                  *(_DWORD *)(v91 + 8) = -1;
                  *(_DWORD *)(v91 + 16) = 0;
                }
              }
              *(_QWORD *)(v89 + 296) = 0;
LABEL_67:
              ++v48;
            }
            while ( v48 != v49 );
          }
        }
      }
      *(_BYTE *)v522 = 0;
      v115 = v520;
      v116 = (__int64)(*(_QWORD *)(*(_QWORD *)(v520 + 128) + 8LL) - **(_QWORD **)(v520 + 128)) >> 3;
      v117 = 0;
      if ( (unsigned int)v116 >= 2 )
      {
        v117 = 0;
        for ( j = 1; (unsigned int)v116 != j; ++j )
        {
          v119 = **(_QWORD **)(v115 + 128);
          if ( *(_QWORD *)(v119 + 8LL * v117) != 0 )
          {
            sub_140FFA860(a1: v115, a2: v117, a3: v117);
          }
          else
          {
            v120 = *(_QWORD *)(v119 + 8 * j);
            v523 = v120;
            if ( v120 == 0 )
              continue;
            sub_140FFA860(a1: v115, a2: v117, a3: *(unsigned int *)(v120 + 8));
            v121 = *(_QWORD **)(v115 + 128);
            if ( (__int64)(v121[1] - *v121) >> 3 > (unsigned __int64)v117 )
            {
              v122 = *(void (__fastcall ****)(_QWORD, __int64))(*v121 + 8LL * v117);
              if ( v122 != nullptr )
                (**v122)(a1: v122, a2: 1);
            }
            sub_14083D020(a1: v121, a2: &v523, a3: v117);
            v115 = v520;
            v123 = *(_QWORD *)(v520 + 128);
            v525[0] = 0;
            sub_14083D020(a1: v123, a2: v525, a3: j);
            *(_DWORD *)(v120 + 8) = v117;
          }
          ++v117;
        }
      }
      if ( v117 < (unsigned int)v116 )
      {
        v124 = *(__int64 **)(v520 + 128);
        v125 = v117;
        v126 = *v124;
        if ( *(_QWORD *)(*v124 + 8 * v125) == 0 )
        {
          v127 = v126 + 8 * v125;
          v128 = (unsigned int)(v116 - 1);
          v129 = v126 + 8 * v128 + 8;
          if ( v127 != v129 )
          {
            v130 = 8 * v125;
            do
            {
              v131 = *(void (__fastcall ****)(_QWORD, __int64))(v126 + v130);
              if ( v131 != nullptr )
                (**v131)(a1: v131, a2: 1);
              v130 += 8;
            }
            while ( 8 * v128 + 8 != v130 );
            v178 = v124[1] - v129;
            sub_141758A00(a1: v127, a2: v126 + 8 * v128 + 8, a3: v178);
            v124[1] = v127 + v178;
          }
        }
      }
      v179 = v521;
      v180 = v520;
      if ( v520 != v521[13] )
        goto LABEL_375;
      v181 = v521[103];
      v182 = 0;
      v522 = (__int64)(*(_QWORD *)(*(_QWORD *)(v181 + 128) + 8LL) - **(_QWORD **)(v181 + 128)) >> 3;
      if ( (unsigned int)v522 >= 2 )
      {
        v183 = (unsigned int)v522;
        v182 = 0;
        for ( k = 1; v183 != k; ++k )
        {
          v185 = **(_QWORD **)(v181 + 128);
          if ( *(_QWORD *)(v185 + 8LL * v182) != 0 )
          {
            sub_140FFA860(a1: v181, a2: v182, a3: v182);
          }
          else
          {
            v186 = *(_QWORD *)(v185 + 8 * k);
            v523 = v186;
            if ( v186 == 0 )
              continue;
            sub_140FFA860(a1: v181, a2: v182, a3: *(unsigned int *)(v186 + 8));
            v187 = *(_QWORD **)(v181 + 128);
            if ( (__int64)(v187[1] - *v187) >> 3 > (unsigned __int64)v182 )
            {
              v188 = *(_QWORD *)(*v187 + 8LL * v182);
              if ( v188 != 0 )
                sub_140E41800(a1: v188);
            }
            sub_14083D020(a1: v187, a2: &v523, a3: v182);
            v189 = *(_QWORD *)(v181 + 128);
            v525[0] = 0;
            sub_14083D020(a1: v189, a2: v525, a3: k);
            *(_DWORD *)(v186 + 8) = v182;
          }
          ++v182;
        }
      }
      v190 = v521;
      if ( v182 < (unsigned int)v522 )
      {
        v191 = *(__int64 **)(v181 + 128);
        v192 = *v191;
        if ( *(_QWORD *)(*v191 + 8LL * v182) == 0 )
        {
          v193 = v192 + 8LL * v182;
          v194 = (unsigned int)(v522 - 1);
          v195 = v192 + 8 * v194 + 8;
          if ( v193 != v195 )
          {
            v196 = 8 * v194 + 8;
            v197 = 8LL * v182;
            do
            {
              v198 = *(_QWORD *)(v192 + v197);
              if ( v198 != 0 )
                sub_140E41800(a1: v198);
              v197 += 8;
            }
            while ( v196 != v197 );
            v199 = v191[1] - v195;
            sub_141758A00(a1: v193, a2: v195, a3: v199);
            v191[1] = v193 + v199;
          }
        }
      }
      v200 = v190[104];
      v201 = 0;
      v515 = (__int64)(*(_QWORD *)(*(_QWORD *)(v200 + 128) + 8LL) - **(_QWORD **)(v200 + 128)) >> 3;
      if ( (unsigned int)v515 >= 2 )
      {
        v202 = (unsigned int)v515;
        v203 = 1;
        v204 = 0;
        v201 = 0;
        v522 = (unsigned int)v515;
        do
        {
          v205 = **(_QWORD **)(v200 + 128);
          if ( *(_QWORD *)(v205 + 8LL * v201) != 0 )
          {
            sub_140FFA860(a1: v200, a2: v201, a3: v201);
            ++v201;
          }
          else
          {
            v206 = *(volatile signed __int32 **)(v205 + v204 * 8 + 8);
            v523 = (__int64)v206;
            if ( v206 != nullptr )
            {
              sub_140FFA860(a1: v200, a2: v201, a3: *((unsigned int *)v206 + 2));
              v207 = *(_QWORD **)(v200 + 128);
              if ( (__int64)(v207[1] - *v207) >> 3 > (unsigned __int64)v201 )
              {
                v208 = *(_QWORD *)(*v207 + 8LL * v201);
                if ( v208 != 0 )
                  sub_140F6BAB0(a1: v208);
              }
              sub_14083D020(a1: v207, a2: &v523, a3: v201);
              v209 = *(_QWORD **)(v200 + 128);
              v210 = (_QWORD **)*v209;
              v211 = v209[1];
              v212 = (v211 - *v209) >> 3;
              if ( v212 > v203 )
                goto LABEL_351;
              v213 = v203 + 1;
              if ( v203 + 1 < v212 )
              {
                v209[1] = &v210[v204 + 2];
LABEL_351:
                v210[v204 + 1] = nullptr;
                *((_DWORD *)v206 + 2) = v201++;
                v202 = v522;
                goto LABEL_324;
              }
              v214 = (__int64)(v209[2] - (_QWORD)v210) >> 3;
              if ( v214 > v203 )
              {
                v215 = 8 * v212;
                v516 = (_QWORD *)(v211 - v215 + v204 * 8 + 16);
                sub_141758A10(a1: v211, a2: 0, a3: v204 * 8 - v215 + 16);
                v209[1] = v516;
                v210 = (_QWORD **)*v209;
                goto LABEL_351;
              }
              if ( v203 >= 0x1FFFFFFFFFFFFFFFLL )
                sub_1400526C0(a1: 0x1FFFFFFFFFFFFFFFLL, a2: v210, a3: v213);
              v516 = *(_QWORD **)(v200 + 128);
              v216 = v214 + (v214 >> 1);
              if ( v216 <= v213 )
                v216 = v203 + 1;
              if ( v214 > 0x1FFFFFFFFFFFFFFFLL - (v214 >> 1) )
                v216 = 0x1FFFFFFFFFFFFFFFLL;
              v512 = v216;
              v217 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v216);
              sub_141758A10(a1: v217 + 8 * v212, a2: 0, a3: v204 * 8 - 8 * v212 + 16);
              v218 = *v516;
              v219 = v516[1] - *v516;
              v511 = (_QWORD **)v217;
              sub_141758A00(a1: v217, a2: v218, a3: v219);
              v220 = v516;
              v221 = *v516;
              if ( *v516 != 0 )
              {
                v222 = v516[2] - v221;
                if ( v222 == -1 )
                  v222 = *(unsigned int *)(v221 - *(unsigned int *)(qword_141ABD470 + 48));
                if ( *(_BYTE *)(qword_141ABD470 + 52) == 0
                  || (v223 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v223) >> 3 <= v222)
                  || (v224 = *(_QWORD *)(v223 + 8 * v222)) == 0 )
                {
                  MEMORY[0x141948990](a1: v221 - *(unsigned int *)(qword_141ABD470 + 48));
                  goto LABEL_349;
                }
                MEMORY[0x1419475D8](a1: v224 + 32, a2: v221 - *(unsigned int *)(v224 + 120));
                v225 = *(_BYTE *)(v224 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v224 + 64)) != 0;
                v220 = v516;
                if ( !v225 && *(_BYTE *)(v224 + 97) != 0 )
                {
                  sub_1412D33C0(a1: v224);
LABEL_349:
                  v220 = v516;
                }
              }
              v210 = v511;
              *v220 = v511;
              v220[1] = &v210[v204 + 2];
              v220[2] = &v210[v512];
              v206 = (volatile signed __int32 *)v523;
              goto LABEL_351;
            }
          }
LABEL_324:
          ++v203;
          ++v204;
        }
        while ( v202 != v203 );
      }
      if ( v201 < (unsigned int)v515 )
      {
        v226 = *(__int64 **)(v200 + 128);
        v227 = *v226;
        if ( *(_QWORD *)(*v226 + 8LL * v201) == 0 )
        {
          v228 = v227 + 8LL * v201;
          v229 = (unsigned int)(v515 - 1);
          v230 = v227 + 8 * v229 + 8;
          if ( v228 != v230 )
          {
            v231 = 8 * v229 + 8;
            v232 = 8LL * v201;
            do
            {
              v233 = *(_QWORD *)(v227 + v232);
              if ( v233 != 0 )
                sub_140F6BAB0(a1: v233);
              v232 += 8;
            }
            while ( v231 != v232 );
            v234 = v226[1] - v230;
            sub_141758A00(a1: v228, a2: v230, a3: v234);
            v226[1] = v228 + v234;
          }
        }
      }
      v179 = v521;
      v180 = v520;
      if ( (qword_141B5E548 & 1) == 0 && (unsigned __int8)sub_140087040() == 0 )
      {
        v235 = v521[199];
        if ( v521[200] != v235 )
        {
          v236 = 0;
          do
          {
            if ( *(_DWORD *)(v235 + 4 * v236) != -1 )
            {
              v237 = sub_1400568B0(a1: qword_141B5FE10);
              if ( v237 != 0 )
              {
                v238 = v237;
                if ( (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v237 + 1720LL))(a1: v237) != 0 )
                {
                  v239 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v238 + 1720LL))(a1: v238);
                  *(_BYTE *)(v239 + 616) |= 1u;
                }
              }
            }
            ++v236;
            v235 = v179[199];
          }
          while ( v236 < (v179[200] - v235) >> 2 );
        }
      }
      v240 = v179[199];
      if ( v240 != v179[200] )
        v179[200] = v240;
LABEL_375:
      v241 = **(__int64 ***)(*(_QWORD *)(qword_141ABD878 + 24) + 8LL);
      v242 = (__int64 *)v241[1];
      v243 = v241;
      if ( *((_BYTE *)v242 + 25) == 0 )
      {
        v243 = **(__int64 ***)(*(_QWORD *)(qword_141ABD878 + 24) + 8LL);
        do
        {
          v244 = v242 + 2;
          if ( v242[4] >= (unsigned __int64)qword_141B5EDF0 )
          {
            v243 = v242;
            v244 = v242;
          }
          v242 = (__int64 *)*v244;
        }
        while ( *(_BYTE *)(*v244 + 25) == 0 );
      }
      if ( *((_BYTE *)v243 + 25) != 0 || qword_141B5EDF0 < (unsigned __int64)v243[4] || v243 == v241 )
      {
        v513 = 0;
      }
      else
      {
        v269 = v243[5];
        v513 = v269;
        if ( v269 != 0 )
          _InterlockedIncrement((volatile signed __int32 *)(v269 + 8));
      }
      v245 = qword_141B5E548;
      if ( (qword_141B5E548 & 2) == 0 )
      {
        v246 = (unsigned __int8)v514;
        sub_140F3BD20(a1: v179, a2: &v513, a3: (unsigned __int8)v514);
        sub_140F3BF60(a1: v179, a2: &v513, a3: v246);
        v245 = qword_141B5E548;
      }
      v247 = v179[13];
      v179[13] = v180;
      v248 = sub_14083D4F0();
      v524 = v245 >> 7;
      v523 = v248 + 24;
      v249 = qword_141B60C30;
      if ( qword_141B60C30 == qword_141B60C38 )
        goto LABEL_387;
      while ( *(_DWORD *)v249 != 1198679666 )
      {
        v249 += 16;
        if ( v249 == qword_141B60C38 )
          goto LABEL_387;
      }
      if ( v249 == qword_141B60C38 || (v270 = *(volatile signed __int32 ***)(v249 + 8)) == nullptr )
      {
LABEL_387:
        sub_140835A40(a1: &qword_141B60C30, a2: 1198679666, a3: &v523);
      }
      else if ( v270 != (volatile signed __int32 **)&v523 )
      {
        (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)*v270 + 16LL))(
          a1: *v270,
          a2: v270);
        (*(void (__fastcall **)(__int64, __int64 *, volatile signed __int32 **))(*(_QWORD *)v523 + 24LL))(
          a1: v523,
          a2: &v523,
          a3: v270);
      }
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v523 + 16LL))(a1: v523, a2: &v523);
      v250 = sub_140087040();
      v251 = sub_14083D4F0();
      v524 = v250;
      v523 = v251 + 24;
      v252 = qword_141B60C30;
      if ( qword_141B60C30 == qword_141B60C38 )
        goto LABEL_391;
      while ( *(_DWORD *)v252 != 1094992708 )
      {
        v252 += 16;
        if ( v252 == qword_141B60C38 )
          goto LABEL_391;
      }
      if ( v252 == qword_141B60C38 || (v271 = *(volatile signed __int32 ***)(v252 + 8)) == nullptr )
      {
LABEL_391:
        sub_140835A40(a1: &qword_141B60C30, a2: 1094992708, a3: &v523);
      }
      else if ( v271 != (volatile signed __int32 **)&v523 )
      {
        (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)*v271 + 16LL))(
          a1: *v271,
          a2: v271);
        (*(void (__fastcall **)(__int64, __int64 *, volatile signed __int32 **))(*(_QWORD *)v523 + 24LL))(
          a1: v523,
          a2: &v523,
          a3: v271);
      }
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v523 + 16LL))(a1: v523, a2: &v523);
      v253 = sub_14083D4F0();
      v524 = 1;
      v523 = v253 + 24;
      v254 = qword_141B60C30;
      if ( qword_141B60C30 == qword_141B60C38 )
        goto LABEL_395;
      while ( *(_DWORD *)v254 != 1314013776 )
      {
        v254 += 16;
        if ( v254 == qword_141B60C38 )
          goto LABEL_395;
      }
      if ( v254 == qword_141B60C38 || (v272 = *(volatile signed __int32 ***)(v254 + 8)) == nullptr )
      {
LABEL_395:
        sub_140835A40(a1: &qword_141B60C30, a2: 1314013776, a3: &v523);
      }
      else if ( v272 != (volatile signed __int32 **)&v523 )
      {
        (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)*v272 + 16LL))(
          a1: *v272,
          a2: v272);
        (*(void (__fastcall **)(__int64, __int64 *, volatile signed __int32 **))(*(_QWORD *)v523 + 24LL))(
          a1: v523,
          a2: &v523,
          a3: v272);
      }
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v523 + 16LL))(a1: v523, a2: &v523);
      v255 = v179[225] - v179[224];
      if ( v255 != 0 )
      {
        v256 = v255 >> 3;
        v257 = 1;
        if ( v256 >= 2 )
          v257 = v256;
        for ( m = 0; m != v257; ++m )
        {
          v259 = *(_QWORD **)(v179[224] + 8 * m);
          v260 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *, _QWORD))(*(_QWORD *)*v259 + 176LL))(
                   a1: *v259,
                   a2: v259,
                   a3: 0);
          sub_140F47AD0(
            a1: (_DWORD)v179,
            a2: v260,
            a3: 0,
            a4: 0,
            a5: 0,
            a6: 1,
            a7: 1,
            a8: 0,
            a9: 0,
            a10: 0,
            a11: 0,
            a12: 0);
        }
      }
      sub_140835C40(a1: &qword_141B60C30, a2: 1094992708);
      sub_140835C40(a1: &qword_141B60C30, a2: 1314013776);
      sub_140835C40(a1: &qword_141B60C30, a2: 1198679666);
      v179[13] = v247;
      if ( (qword_141B5E548 & 0x80u) != 0LL )
        goto LABEL_649;
      if ( (unsigned __int8)sub_140087050() != 0 )
      {
        v262 = **(_QWORD **)(*(_QWORD *)(qword_141ABD878 + 24) + 8LL);
        v261 = *(_QWORD *)(v262 + 8);
        v263 = v262;
        if ( *(_BYTE *)(v261 + 25) == 0 )
        {
          v263 = **(_QWORD **)(*(_QWORD *)(qword_141ABD878 + 24) + 8LL);
          do
          {
            v264 = (__int64 *)(v261 + 16);
            if ( *(_QWORD *)(v261 + 32) >= (unsigned __int64)qword_141B59838 )
            {
              v263 = v261;
              v264 = (__int64 *)v261;
            }
            v261 = *v264;
          }
          while ( *(_BYTE *)(*v264 + 25) == 0 );
        }
        if ( *(_BYTE *)(v263 + 25) == 0 )
        {
          v261 = qword_141B59838;
          if ( (unsigned __int64)qword_141B59838 >= *(_QWORD *)(v263 + 32) && v263 != v262 )
          {
            v380 = *(volatile signed __int32 **)(v263 + 40);
            if ( v380 != nullptr )
            {
              _InterlockedIncrement(v380 + 2);
              sub_14080D0E0(a1: &v523, a2: 0x1418DF862LL);
              v381 = sub_1412EC810(a1: 264, a2: 17);
              *(_QWORD *)v381 = 0x1100000000LL;
              strcpy((char *)(v381 + 8), "person_db_changes");
              _InterlockedIncrement((volatile signed __int32 *)v381);
              v525[0] = 0;
              _InterlockedIncrement((volatile signed __int32 *)v381);
              v525[0] = v381 + 4;
              v382 = (*(__int64 (__fastcall **)(volatile signed __int32 *, _QWORD *, __int64 *))(*(_QWORD *)v380 + 192LL))(
                       a1: v380,
                       a2: v525,
                       a3: &v523);
              v383 = v525[0];
              if ( v525[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v525[0] - 4LL)) == 0 )
                sub_1412EC9A0(a1: v383 - 4);
              if ( _InterlockedDecrement((volatile signed __int32 *)v381) == 0 )
                sub_1412EC9A0(a1: v381);
              if ( v382 == 0 )
              {
                sub_14080D0E0(a1: &v518, a2: 0x1418DF862LL);
                v384 = sub_1412EC810(a1: 264, a2: 17);
                *(_QWORD *)v384 = 0x1100000000LL;
                strcpy((char *)(v384 + 8), "person_db_changes");
                _InterlockedIncrement((volatile signed __int32 *)v384);
                v517 = 0;
                _InterlockedIncrement((volatile signed __int32 *)v384);
                v517 = v384 + 4;
                v525[0] = 0x80100004E554C4CLL;
                (*(void (__fastcall **)(volatile signed __int32 *, __int64 *, __int64 *, volatile signed __int32 **))(*(_QWORD *)v380 + 224LL))(
                  a1: v380,
                  a2: &v523,
                  a3: &v517,
                  a4: &v518);
                if ( v523 != 0 )
                {
                  LOWORD(v385) = 3569;
                  sub_1407D1280(
                    a1: (unsigned int)v525,
                    a2: (unsigned int)&v519,
                    a3: (unsigned int)&v523,
                    a4: v385,
                    a5: 0);
                  v386 = (void (__fastcall ***)(_QWORD, __int64))v523;
                  v387 = v179;
                  if ( v523 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v523 + 8)) == 0 )
                    (**v386)(a1: v386, a2: 1);
                }
                else
                {
                  v519 = nullptr;
                  v387 = v179;
                }
                v495 = v517;
                if ( v517 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v517 - 4)) == 0 )
                  sub_1412EC9A0(a1: v495 - 4);
                if ( _InterlockedDecrement((volatile signed __int32 *)v384) == 0 )
                  sub_1412EC9A0(a1: v384);
                v496 = v519;
                if ( v519 != nullptr )
                {
                  LODWORD(v523) = (v387[225] - v387[224]) >> 3;
                  (*(void (__fastcall **)(volatile signed __int32 *, __int64 *, __int64))(*(_QWORD *)v519 + 40LL))(
                    a1: v519,
                    a2: &v523,
                    a3: 4);
                  if ( *((_DWORD *)v496 + 4) == 0 )
                  {
                    v499 = v387[224];
                    v500 = v387[225];
                    if ( v499 != v500 )
                    {
                      v501 = v499 + 8;
                      do
                      {
                        sub_140838050(a1: v496, a2: &v523, a3: *(_QWORD *)(v501 - 8));
                        if ( (_DWORD)v523 != 0 )
                          break;
                        if ( v501 == v500 )
                          break;
                        v501 += 8;
                      }
                      while ( *((_DWORD *)v496 + 4) == 0 );
                    }
                  }
                  v497 = v519;
                  if ( v519 != nullptr && _InterlockedDecrement(v519 + 2) == 0 )
                    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v497)(a1: v497, a2: 1);
                }
              }
              v498 = _InterlockedDecrement(v380 + 2);
              v180 = v520;
              if ( v498 == 0 )
                (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v380)(a1: v380, a2: 1);
            }
          }
        }
      }
      v265 = (_QWORD *)v179[224];
      v266 = (_QWORD *)v179[225];
      if ( v265 != v266 )
      {
        v267 = (_QWORD *)v179[224];
        do
        {
          v268 = (_QWORD *)*v267;
          if ( *v267 != 0 )
          {
            (*(void (__fastcall **)(_QWORD, _QWORD))(*(_QWORD *)*v268 + 16LL))(a1: *v268, a2: *v267);
            sub_1408B5E70(a1: v268);
          }
          ++v267;
        }
        while ( v267 != v266 );
        v273 = v179[225] - (_QWORD)v266;
        sub_141758A00(a1: v265, a2: v266, a3: v273);
        v179[225] = (char *)v265 + v273;
      }
      if ( v180 == v179[13] )
      {
        LOBYTE(v261) = 8;
        if ( (qword_141B5E548 & 2) != 0 )
        {
          *(_BYTE *)(v180 + 89) = 1;
          LOBYTE(v261) = 32;
        }
        sub_140F3C890(a1: v179, a2: v261);
      }
      v274 = *(unsigned int ****)(qword_141B5FE10 + 128);
      v275 = *v274;
      v276 = v274[1];
      if ( *v274 != v276 )
      {
        while ( 1 )
        {
          v278 = *v275;
          if ( (*(__int64 (__fastcall **)(unsigned int *))(*(_QWORD *)*v275 + 1816LL))(a1: *v275) != 0 )
            break;
LABEL_440:
          if ( ++v275 == v276 )
            goto LABEL_464;
        }
        if ( dword_141B5F3E0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                         + 4LL) )
        {
          sub_141750E08(a1: &dword_141B5F3E0);
          if ( dword_141B5F3E0 == -1 )
          {
            sub_1407E53D0(
              a1: (unsigned int)&unk_141B5F390,
              a2: 1100130726,
              a3: 0x4000,
              a4: 48,
              a5: 0,
              a6: 0,
              a7: 1024,
              a8: 4096);
            sub_141751048(a1: sub_140FB3BA0);
            sub_141750EA0(a1: &dword_141B5F3E0);
          }
        }
        v279 = sub_1407E58C0(a1: &unk_141B5F390, a2: 48);
        v281 = v278[3];
        v282 = v278[4];
        if ( v282 == 0 )
          v282 = v278[3];
        v283 = v279;
        *(_DWORD *)(v279 + 8) = -1;
        *(_QWORD *)(v279 + 24) = 0;
        *(_QWORD *)v279 = 0x14188A548LL;
        v284 = (__int64 *)(v279 + 32);
        v285 = (__int64 *)(v283 + 40);
        *(_QWORD *)(v283 + 32) = 0;
        *(_QWORD *)(v283 + 40) = 0;
        *(_DWORD *)(v283 + 12) = v281;
        *(_DWORD *)(v283 + 16) = v282;
        v286 = qword_141B59EE0;
        if ( qword_141B59EE0 != 0 )
        {
          if ( v284 == &qword_141B59EE0 || *(_DWORD *)qword_141B59EE0 != 0 )
            goto LABEL_451;
          _InterlockedIncrement((volatile signed __int32 *)(qword_141B59EE0 - 4));
        }
        else if ( v284 == &qword_141B59EE0 )
        {
LABEL_451:
          if ( v285 != &qword_141B59EE0 )
          {
            v287 = *v285;
            v288 = (volatile signed __int32 *)(*v285 - 4);
            if ( *v285 == 0 )
              v288 = nullptr;
            v289 = (volatile signed __int32 *)(qword_141B59EE0 - 4);
            if ( qword_141B59EE0 != 0 )
            {
              if ( v287 != 0 && _InterlockedDecrement(v288) == 0 )
                sub_1412EC9A0(a1: v288);
              *v285 = 0;
              _InterlockedIncrement(v289);
              v277 = v289 + 1;
            }
            else
            {
              if ( v287 != 0 && _InterlockedDecrement(v288) == 0 )
                sub_1412EC9A0(a1: v288);
              v277 = nullptr;
            }
            *v285 = (__int64)v277;
          }
          LOBYTE(v280) = 1;
          sub_140F68D60(a1: v521, a2: v283, a3: v278[2], a4: v280);
          goto LABEL_440;
        }
        *v284 = v286;
        goto LABEL_451;
      }
LABEL_464:
      v179 = v521;
      v290 = (_QWORD *)v521[191];
      v291 = (_QWORD *)v290[1];
      v292 = v291;
      if ( v291 != (_QWORD *)*v290 )
      {
        v293 = (((__int64)v291 - *v290) >> 3) - 1;
        do
        {
          v295 = (__int64 *)v179[191];
          v296 = *v295;
          v297 = *(_QWORD *)(*v295 + 8 * v293);
          if ( (*(_BYTE *)(v297 + 26) & 0x40) == 0 )
          {
            v523 = 0;
            if ( (v295[1] - v296) >> 3 > v293 )
              (**(void (__fastcall ***)(__int64, __int64))v297)(a1: v297, a2: 1);
            sub_14083D020(a1: v295, a2: &v523, a3: v293);
          }
        }
        while ( v293-- != 0 );
        v290 = (_QWORD *)v179[191];
        v291 = (_QWORD *)*v290;
        v292 = (_QWORD *)v290[1];
      }
      v298 = (_QWORD *)sub_141751B70(a1: v291, a2: v292, a3: 0);
      v299 = v298;
      if ( v298 != v292 )
      {
        while ( ++v298 != v292 )
        {
          if ( *v298 != 0 )
            *v299++ = *v298;
        }
      }
      if ( v299 != v292 )
      {
        v300 = v290[1] - (_QWORD)v292;
        sub_141758A00(a1: v299, a2: v292, a3: v300);
        v290[1] = (char *)v299 + v300;
      }
      v301 = qword_141B5E548;
      if ( (qword_141B5E548 & 0x10) != 0 )
      {
        if ( qword_141ABD470 == 0 )
        {
          if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer
                                             + (unsigned int)TlsIndex)
                                           + 4LL) )
          {
            sub_141750E08(a1: &dword_141B59AA8);
            if ( dword_141B59AA8 == -1 )
            {
              sub_1407E3E70(a1: &unk_141B59A68);
              sub_141751048(a1: sub_1407E4B20);
              sub_141750EA0(a1: &dword_141B59AA8);
              v179 = v521;
            }
          }
          qword_141ABD470 = (__int64)&unk_141B59A68;
        }
        v302 = *(_QWORD *)(*(_QWORD *)(v179[13] + 128LL) + 8LL) - **(_QWORD **)(v179[13] + 128LL);
        if ( v302 != 0 )
        {
          v303 = v302 >> 3;
          v304 = 1;
          if ( v303 >= 2 )
            v304 = v303;
          for ( n = 0; n != v304; ++n )
          {
            v306 = *(_QWORD *)(**(_QWORD **)(v179[13] + 128LL) + 8 * n);
            v307 = (*(__int64 (__fastcall **)(__int64, _QWORD))(*(_QWORD *)v306 + 416LL))(a1: v306, a2: 0);
            if ( v307 != 0 )
            {
              v308 = *(_WORD *)(v307 + 14);
              if ( v308 > 0 )
                *(_WORD *)(v307 + 14) = -v308;
            }
            v309 = (*(__int64 (__fastcall **)(__int64, _QWORD))(*(_QWORD *)v306 + 424LL))(a1: v306, a2: 0);
            if ( v309 != 0 )
            {
              v310 = *(_WORD *)(v309 + 14);
              if ( v310 > 0 )
                *(_WORD *)(v309 + 14) = -v310;
            }
            v311 = (*(__int64 (__fastcall **)(__int64, _QWORD))(*(_QWORD *)v306 + 432LL))(a1: v306, a2: 0);
            if ( v311 != 0 )
            {
              v312 = *(_WORD *)(v311 + 14);
              if ( v312 > 0 )
                *(_WORD *)(v311 + 14) = -v312;
            }
          }
        }
        v507 = (char ***)(v179 + 26);
        v511 = (_QWORD **)(v179 + 25);
        v508 = (char ***)(v179 + 27);
        v313 = -1;
        v314 = nullptr;
        v514 = nullptr;
        v315 = nullptr;
        v520 = 0;
        while ( 1 )
        {
          v316 = (char ***)v511;
          if ( (_BYTE)v314 != 0 )
          {
            v316 = v507;
            if ( (unsigned __int8)v314 != 1 )
              v316 = v508;
          }
          v317 = (__int64 *)*v316;
          v318 = **v316;
          v319 = (*v316)[1];
          if ( v319 != v318 )
            break;
          v522 = (__int64)v315;
          v318 = v319;
LABEL_561:
          v349 = (char *)sub_141751B70(a1: v318, a2: v319, a3: 0);
          v350 = v349;
          if ( v349 != v319 )
          {
            while ( 1 )
            {
              v349 += 8;
              if ( v349 == v319 )
                break;
              if ( *(_QWORD *)v349 != 0 )
                *v350++ = *(_QWORD *)v349;
            }
          }
          v351 = (char *)v317[1];
          if ( v350 != (_QWORD *)v319 )
          {
            v352 = v351 - v319;
            sub_141758A00(a1: v350, a2: v319, a3: v352);
            v351 = (char *)v350 + v352;
            v317[1] = (__int64)v351;
          }
          v315 = (char *)v522;
          v353 = (__int64)&v351[-*v317];
          if ( v353 != 0 )
          {
            v354 = v353 >> 3;
            if ( v354 < 2 )
              v354 = 1;
            v355 = v354 & 3;
            if ( v354 - 1 >= 3 )
            {
              v357 = v354 & 0xFFFFFFFFFFFFFFFCuLL;
              v356 = 0;
              do
              {
                *(_DWORD *)(*(_QWORD *)(*v317 + 8 * v356) + 8LL) = v356;
                *(_DWORD *)(*(_QWORD *)(*v317 + 8 * v356 + 8) + 8LL) = v356 + 1;
                *(_DWORD *)(*(_QWORD *)(*v317 + 8 * v356 + 16) + 8LL) = v356 + 2;
                *(_DWORD *)(*(_QWORD *)(*v317 + 8 * v356 + 24) + 8LL) = v356 + 3;
                v356 += 4;
              }
              while ( v356 != v357 );
            }
            else
            {
              v356 = 0;
            }
            for ( ; v355 != 0; --v355 )
            {
              *(_DWORD *)(*(_QWORD *)(*v317 + 8 * v356) + 8LL) = v356;
              ++v356;
            }
          }
          LOBYTE(v314) = (_BYTE)v314 + 1;
          if ( (_BYTE)v314 == 3 )
          {
            v358 = *(_QWORD *)(v179[198] + 8LL) - *(_QWORD *)v179[198];
            if ( v358 != 0 )
            {
              v359 = v358 >> 3;
              v360 = -(__int64)(v358 & 0xFFFFFFFFFFFFFFF8uLL);
              do
              {
                v361 = v359--;
                v362 = v179;
                v363 = (__int64 *)v179[198];
                v364 = *v363;
                v365 = *(_QWORD **)(*v363 + 8 * v361 - 8);
                v366 = v365[1];
                if ( v366 != 0 && (*(_BYTE *)(v366 + 18) & 0x10) != 0
                  || *v365 != 0 && (*(_BYTE *)(*v365 + 18LL) & 0x10) != 0 )
                {
                  sub_140F6E590();
                  sub_141758A00(a1: v364 + 8 * v361 - 8, a2: v364 + 8 * v361, a3: v360 + v363[1] - v364);
                  v315 = (char *)v522;
                  v363[1] -= 8;
                }
                v360 += 8;
                v179 = v362;
              }
              while ( v359 != 0 );
            }
            v367 = v514;
            if ( v514 != v315 )
            {
              do
              {
                v368 = *(__int64 **)v367;
                if ( *(_QWORD *)v367 != 0 )
                {
                  v369 = *v368;
                  if ( *v368 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v369 - 4)) == 0 )
                    sub_1412EC9A0(a1: v369 - 4);
                  sub_140E050C0(a1: v368);
                  v315 = (char *)v522;
                }
                v367 += 8;
              }
              while ( v367 != v315 );
              v315 = v514;
            }
            if ( v315 != nullptr )
            {
              v370 = v520 - (_QWORD)v315;
              if ( v520 - (_QWORD)v315 == -1 )
                v370 = *(unsigned int *)&v315[-*(unsigned int *)(qword_141ABD470 + 48)];
              if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                && (v371 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v371) >> 3 > v370)
                && (v372 = *(_QWORD *)(v371 + 8 * v370)) != 0 )
              {
                MEMORY[0x1419475D8](a1: v372 + 32, a2: &v315[-*(unsigned int *)(v372 + 120)]);
                v373 = *(_BYTE *)(v372 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v372 + 64)) != 0;
                if ( !v373 && *(_BYTE *)(v372 + 97) != 0 )
                  sub_1412D33C0(a1: v372);
              }
              else
              {
                MEMORY[0x141948990](a1: &v315[-*(unsigned int *)(qword_141ABD470 + 48)]);
              }
            }
            v301 = qword_141B5E548;
            goto LABEL_605;
          }
        }
        v516 = v314;
        v320 = 0;
        v321 = 0;
        while ( 1 )
        {
          v323 = *(_QWORD *)&v318[8 * v320];
          v324 = *(__int16 *)(v323 + 12);
          if ( v313 != v324 )
            v321 = 0;
          v325 = *(_WORD *)(v323 + 14);
          if ( v325 <= 0 || v321 <= 998 && v325 != 1 || v321 <= 248 && v325 == 1 )
          {
            v322 = -v325;
            if ( v325 > 0 )
              v322 = *(_WORD *)(v323 + 14);
            *(_WORD *)(v323 + 14) = v322;
            goto LABEL_506;
          }
          if ( v315 != (char *)v520 )
          {
            *(_QWORD *)v315 = v323;
            v315 += 8;
            goto LABEL_532;
          }
          v326 = v514;
          v327 = v315 - v514;
          v328 = (unsigned __int64)(v327 >> 3) >> 1;
          v329 = 0x1FFFFFFFFFFFFFFFLL - v328;
          v330 = (v327 >> 3) + v328;
          v520 = (v327 >> 3) + 1;
          if ( v330 <= v520 )
            v330 = (v327 >> 3) + 1;
          if ( v327 >> 3 > v329 )
            v330 = 0x1FFFFFFFFFFFFFFFLL;
          v515 = v330;
          v331 = v327;
          v332 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v330);
          *(_QWORD *)(v332 + v331) = v323;
          v522 = v332;
          sub_141758A00(a1: v332, a2: v326, a3: v331);
          if ( v326 != nullptr )
            break;
LABEL_531:
          v315 = (char *)(v522 + 8 * v520);
          v520 = v522 + 8 * v515;
          v514 = (char *)v522;
LABEL_532:
          *(_BYTE *)(v323 + 18) |= 0x10u;
          v335 = *v317;
          v336 = v317[1];
          v337 = (v336 - *v317) >> 3;
          if ( v337 <= v320 )
          {
            v338 = v320 + 1;
            v339 = v320 + 1 - v337;
            if ( v320 + 1 >= v337 )
            {
              v340 = (v317[2] - v335) >> 3;
              if ( v340 <= v320 )
              {
                v522 = (__int64)v315;
                if ( v320 >= 0x1FFFFFFFFFFFFFFFLL )
                  sub_1400526C0(a1: v336, a2: 0x1FFFFFFFFFFFFFFFLL, a3: v339);
                v343 = v340 + (v340 >> 1);
                v515 = v320 + 1;
                if ( v343 <= v338 )
                  v343 = v320 + 1;
                if ( v340 > 0x1FFFFFFFFFFFFFFFLL - (v340 >> 1) )
                  v343 = 0x1FFFFFFFFFFFFFFFLL;
                v512 = v343;
                v344 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v343);
                sub_141758A10(a1: v344 + 8 * v337, a2: 0, a3: 8 * (v320 + 1 - v337));
                v335 = v344;
                sub_141758A00(a1: v344, a2: *v317, a3: v317[1] - *v317);
                v345 = *v317;
                if ( *v317 != 0 )
                {
                  v346 = v317[2] - v345;
                  if ( v346 == -1 )
                  {
                    v346 = *(unsigned int *)(v345 - *(unsigned int *)(qword_141ABD470 + 48));
                    if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
                      goto LABEL_552;
                  }
                  else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
                  {
                    goto LABEL_552;
                  }
                  v347 = *(_QWORD *)(qword_141ABD470 + 24);
                  if ( (*(_QWORD *)(qword_141ABD470 + 32) - v347) >> 3 > v346
                    && (v348 = *(_QWORD *)(v347 + 8 * v346)) != 0 )
                  {
                    MEMORY[0x1419475D8](a1: v348 + 32, a2: v345 - *(unsigned int *)(v348 + 120));
                    if ( (*(_BYTE *)(v348 + 72) == 0
                       || _InterlockedDecrement((volatile signed __int32 *)(v348 + 64)) == 0)
                      && *(_BYTE *)(v348 + 97) != 0 )
                    {
                      sub_1412D33C0(a1: v348);
                    }
                  }
                  else
                  {
LABEL_552:
                    MEMORY[0x141948990](a1: v345 - *(unsigned int *)(qword_141ABD470 + 48));
                  }
                }
                *v317 = v335;
                v317[1] = v335 + 8 * v515;
                v317[2] = v335 + 8 * v512;
                v315 = (char *)v522;
                goto LABEL_554;
              }
              v341 = v336 + 8 * v339;
              v342 = v315;
              sub_141758A10(a1: v336, a2: 0, a3: 8 * v339);
              v315 = v342;
              v317[1] = v341;
              v335 = *v317;
            }
            else
            {
              v317[1] = v335 + 8 * v338;
            }
          }
LABEL_554:
          *(_QWORD *)(v335 + 8 * v320) = 0;
LABEL_506:
          ++v321;
          ++v320;
          v318 = (char *)*v317;
          v319 = (char *)v317[1];
          v313 = v324;
          if ( v320 >= (__int64)&v319[-*v317] >> 3 )
          {
            v522 = (__int64)v315;
            v313 = v324;
            v179 = v521;
            v314 = v516;
            goto LABEL_561;
          }
        }
        if ( v331 == -1 )
        {
          v331 = *(unsigned int *)&v326[-*(unsigned int *)(qword_141ABD470 + 48)];
          if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
          {
LABEL_530:
            MEMORY[0x141948990](a1: &v326[-*(unsigned int *)(qword_141ABD470 + 48)]);
            goto LABEL_531;
          }
        }
        else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        {
          goto LABEL_530;
        }
        v333 = *(_QWORD *)(qword_141ABD470 + 24);
        if ( (*(_QWORD *)(qword_141ABD470 + 32) - v333) >> 3 > v331 )
        {
          v334 = *(_QWORD *)(v333 + 8 * v331);
          if ( v334 != 0 )
          {
            MEMORY[0x1419475D8](a1: v334 + 32, a2: &v326[-*(unsigned int *)(v334 + 120)]);
            if ( (*(_BYTE *)(v334 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v334 + 64)) == 0)
              && *(_BYTE *)(v334 + 97) != 0 )
            {
              sub_1412D33C0(a1: v334);
            }
            goto LABEL_531;
          }
        }
        goto LABEL_530;
      }
LABEL_605:
      if ( (v301 & 8) == 0 )
        goto LABEL_608;
      if ( (unsigned __int8)sub_1400015B0() != 0 )
      {
        v301 = qword_141B5E548;
LABEL_608:
        if ( (v301 & 2) == 0 )
        {
          v523 = 0;
          v525[0] = 0x80100004E554C4CLL;
          sub_14080D0E0(a1: &v518, a2: 0x1418E2C24LL);
          v374 = sub_1412EC810(a1: 264, a2: 9);
          *(_QWORD *)v374 = 0x900000000LL;
          strcpy((char *)(v374 + 8), "server_db");
          _InterlockedIncrement((volatile signed __int32 *)v374);
          v517 = 0;
          _InterlockedIncrement((volatile signed __int32 *)v374);
          v517 = v374 + 4;
          sub_1407D0F70(
            a1: (unsigned int)v525,
            a2: (unsigned int)&v519,
            a3: (unsigned int)&v513,
            a4: (unsigned int)&v517,
            a5: (__int64)&v518,
            a6: 0,
            a7: 0,
            a8: 0);
          v375 = v517;
          if ( v517 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v517 - 4)) == 0 )
            sub_1412EC9A0(a1: v375 - 4);
          if ( _InterlockedDecrement((volatile signed __int32 *)v374) == 0 )
            sub_1412EC9A0(a1: v374);
          v376 = v519;
          if ( v519 != nullptr )
          {
            v377 = WORD2(v525[0]);
            *((_WORD *)v179 + 708) = WORD2(v525[0]);
            if ( v377 <= 0xDF1 )
            {
              v517 = (__int64)v376;
              _InterlockedIncrement(v376 + 2);
              sub_1407C5A20(a1: &v518, a2: &v517, a3: &v513, a4: &v523);
              v378 = (void (__fastcall ***)(_QWORD, __int64))v517;
              if ( v517 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v517 + 8)) == 0 )
                (**v378)(a1: v378, a2: 1);
              if ( v518 != nullptr )
              {
                if ( (unsigned __int8)sub_1410BAE40(a1: v179[25], a2: &v518) != 0
                  && (unsigned __int8)sub_1410BAE40(a1: v179[26], a2: &v518) != 0 )
                {
                  sub_1410BAE40(a1: v179[27], a2: &v518);
                }
                v379 = v518;
                if ( v518 != nullptr && _InterlockedDecrement(v518 + 2) == 0 )
                  (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v379)(a1: v379, a2: 1);
              }
            }
          }
          else
          {
            sub_140F2B090();
          }
          v388 = v519;
          if ( v519 != nullptr && _InterlockedDecrement(v519 + 2) == 0 )
            (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v388)(a1: v388, a2: 1);
          v389 = (volatile signed __int32 *)v523;
          if ( v523 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v523 - 4)) == 0 )
            sub_1412EC9A0(a1: v389 - 1);
          if ( a5 != 0 )
          {
            sub_140F56290(a1: v179);
            LOBYTE(v504) = 0;
            sub_140F500A0(a1: (_DWORD)v179, a2: v509, a3: (unsigned int)&unk_141B5E460, a4: 0, a5: 0, a6: v504, a7: 0);
            sub_140F6A050(a1: v179);
            LOBYTE(v505) = 0;
            sub_140F500A0(a1: (_DWORD)v179, a2: v509, a3: (unsigned int)&unk_141B5E468, a4: 0, a5: 0, a6: v505, a7: 0);
          }
        }
        sub_1410BB5F0(a1: v179[25], a2: v179 + 53);
        sub_1410BB5F0(a1: v179[26], a2: v179 + 56);
        sub_1410BB5F0(a1: v179[27], a2: v179 + 59);
        sub_140F40E30(a1: v179);
      }
LABEL_649:
      sub_140F3E890(a1: v179);
      sub_140F46280(a1: v179);
      sub_140F318F0(a1: v179);
      *((_WORD *)v179 + 708) = 3569;
      if ( qword_141ABD470 == 0 )
      {
        if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                         + 4LL) )
        {
          sub_141750E08(a1: &dword_141B59AA8);
          if ( dword_141B59AA8 == -1 )
          {
            sub_1407E3E70(a1: &unk_141B59A68);
            sub_141751048(a1: sub_1407E4B20);
            sub_141750EA0(a1: &dword_141B59AA8);
          }
        }
        qword_141ABD470 = (__int64)&unk_141B59A68;
      }
      qword_141B5E548 = 0;
      v390 = (void (__fastcall ***)(_QWORD, __int64))qword_141B5E550;
      if ( qword_141B5E550 != 0 )
      {
        if ( _InterlockedDecrement((volatile signed __int32 *)(qword_141B5E550 + 8)) == 0 )
          (**v390)(a1: v390, a2: 1);
        qword_141B5E550 = 0;
      }
      if ( qword_141B5E558 != 0 )
      {
        v391 = qword_141B5E568 - qword_141B5E558;
        if ( qword_141B5E568 - qword_141B5E558 == -1 )
          v391 = *(unsigned int *)(qword_141B5E558 - *(unsigned int *)(qword_141ABD470 + 48));
        if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
          && (v392 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v392) >> 3 > v391)
          && (v393 = *(_QWORD *)(v392 + 8 * v391)) != 0 )
        {
          MEMORY[0x1419475D8](a1: v393 + 32, a2: qword_141B5E558 - *(unsigned int *)(v393 + 120));
          v394 = *(_BYTE *)(v393 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v393 + 64)) != 0;
          if ( !v394 && *(_BYTE *)(v393 + 97) != 0 )
            sub_1412D33C0(a1: v393);
        }
        else
        {
          MEMORY[0x141948990](a1: qword_141B5E558 - *(unsigned int *)(qword_141ABD470 + 48));
        }
        qword_141B5E568 = 0;
        qword_141B5E560 = 0;
        qword_141B5E558 = 0;
      }
      qword_141B5E568 = 0;
      qword_141B5E560 = 0;
      qword_141B5E558 = 0;
      if ( qword_141B5E570 != 0 )
      {
        v395 = qword_141B5E580 - qword_141B5E570;
        if ( qword_141B5E580 - qword_141B5E570 == -1 )
          v395 = *(unsigned int *)(qword_141B5E570 - *(unsigned int *)(qword_141ABD470 + 48));
        if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
          && (v396 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v396) >> 3 > v395)
          && (v397 = *(_QWORD *)(v396 + 8 * v395)) != 0 )
        {
          MEMORY[0x1419475D8](a1: v397 + 32, a2: qword_141B5E570 - *(unsigned int *)(v397 + 120));
          v398 = *(_BYTE *)(v397 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v397 + 64)) != 0;
          if ( !v398 && *(_BYTE *)(v397 + 97) != 0 )
            sub_1412D33C0(a1: v397);
        }
        else
        {
          MEMORY[0x141948990](a1: qword_141B5E570 - *(unsigned int *)(qword_141ABD470 + 48));
        }
        qword_141B5E580 = 0;
        qword_141B5E578 = 0;
        qword_141B5E570 = 0;
      }
      qword_141B5E580 = 0;
      qword_141B5E578 = 0;
      qword_141B5E570 = 0;
      if ( qword_141B5E588 != 0 )
      {
        v399 = qword_141B5E598 - qword_141B5E588;
        if ( qword_141B5E598 - qword_141B5E588 == -1 )
          v399 = *(unsigned int *)(qword_141B5E588 - *(unsigned int *)(qword_141ABD470 + 48));
        if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
          && (v400 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v400) >> 3 > v399)
          && (v401 = *(_QWORD *)(v400 + 8 * v399)) != 0 )
        {
          MEMORY[0x1419475D8](a1: v401 + 32, a2: qword_141B5E588 - *(unsigned int *)(v401 + 120));
          v402 = *(_BYTE *)(v401 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v401 + 64)) != 0;
          if ( !v402 && *(_BYTE *)(v401 + 97) != 0 )
            sub_1412D33C0(a1: v401);
        }
        else
        {
          MEMORY[0x141948990](a1: qword_141B5E588 - *(unsigned int *)(qword_141ABD470 + 48));
        }
        qword_141B5E598 = 0;
        qword_141B5E590 = 0;
        qword_141B5E588 = 0;
      }
      qword_141B5E5A0 = 0;
      qword_141B5E598 = 0;
      qword_141B5E590 = 0;
      qword_141B5E588 = 0;
      if ( qword_141B5E5A8 != 0 )
      {
        v403 = qword_141B5E5B8 - qword_141B5E5A8;
        if ( qword_141B5E5B8 - qword_141B5E5A8 == -1 )
          v403 = *(unsigned int *)(qword_141B5E5A8 - *(unsigned int *)(qword_141ABD470 + 48));
        if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
          && (v404 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v404) >> 3 > v403)
          && (v405 = *(_QWORD *)(v404 + 8 * v403)) != 0 )
        {
          MEMORY[0x1419475D8](a1: v405 + 32, a2: qword_141B5E5A8 - *(unsigned int *)(v405 + 120));
          v406 = *(_BYTE *)(v405 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v405 + 64)) != 0;
          if ( !v406 && *(_BYTE *)(v405 + 97) != 0 )
            sub_1412D33C0(a1: v405);
        }
        else
        {
          MEMORY[0x141948990](a1: qword_141B5E5A8 - *(unsigned int *)(qword_141ABD470 + 48));
        }
        qword_141B5E5B8 = 0;
        qword_141B5E5B0 = 0;
        qword_141B5E5A8 = 0;
      }
      qword_141B5E5C8 = 0;
      qword_141B5E5C0 = 0;
      qword_141B5E5B8 = 0;
      qword_141B5E5B0 = 0;
      qword_141B5E5A8 = 0;
      HIDWORD(qword_141B5E548) = 5;
      v166 = v513;
LABEL_697:
      if ( v166 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v166 + 8)) == 0 )
        (**(void (__fastcall ***)(__int64, __int64))v166)(a1: v166, a2: 1);
      return true;
    default:
      return true;
  }
}
