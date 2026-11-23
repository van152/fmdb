__int64 __fastcall sub_14004AF40(__int64 a1, char a2)
{
  _QWORD *v2; // rsi
  __int64 v4; // rdi
  char v5; // bl
  int v6; // r8d
  void (__fastcall ***v7)(_QWORD, __int64); // rcx
  volatile signed __int32 *v8; // rsi
  volatile signed __int32 *v9; // rdi
  int v10; // edi
  int v11; // esi
  _QWORD *v12; // rax
  __int64 v13; // rsi
  __int64 v14; // rdi
  __int64 v15; // rcx
  __int64 v16; // rcx
  int v17; // esi
  bool v18; // bl
  int v19; // esi
  int v20; // esi
  int v21; // esi
  __int64 v22; // rax
  __int64 v23; // rbp
  __int64 v24; // r8
  __int64 v25; // r9
  volatile signed __int32 *v26; // rcx
  __int64 v27; // rax
  unsigned __int64 v28; // rbp
  volatile signed __int32 *v29; // rbx
  __int64 v30; // rax
  __int64 v31; // rdx
  unsigned __int64 v32; // rdx
  __int64 v33; // rcx
  __int64 v34; // rdx
  __int64 v35; // rbp
  __int64 v36; // rbx
  _QWORD *v37; // rdi
  int v38; // eax
  __int64 v39; // rcx
  __int64 v40; // rbp
  __int64 v41; // rsi
  __int64 v42; // rdx
  __int64 v43; // r15
  __int64 v44; // rsi
  __int64 v45; // rax
  __int64 v46; // rdx
  __int64 v47; // rdx
  __int64 v48; // r8
  __int64 v49; // rax
  __int64 v50; // rdx
  unsigned __int64 v51; // rsi
  __int64 v52; // rcx
  int v53; // eax
  __int64 v54; // rax
  __int64 v55; // rcx
  __int64 *v56; // rsi
  int v57; // r8d
  __int64 v58; // r15
  unsigned __int64 v59; // r15
  __int64 i; // r14
  __int64 v61; // rax
  __int64 v62; // rsi
  __int64 v63; // r13
  int v64; // ebx
  unsigned __int64 v65; // rsi
  int v66; // esi
  int v67; // ebp
  __int64 v68; // rcx
  __int64 v69; // rdi
  int v70; // edx
  unsigned __int64 v71; // rsi
  int v72; // esi
  int v73; // ebp
  __int64 v74; // rcx
  __int64 v75; // r12
  int v76; // eax
  int v77; // ebp
  __int64 v78; // rax
  __int64 v79; // rbx
  unsigned __int64 v80; // rbx
  int v81; // ebx
  int v82; // edx
  __int64 v83; // rcx
  int v84; // r8d
  int v85; // eax
  unsigned __int64 v86; // rbx
  int v87; // ebx
  int v88; // edx
  __int64 v89; // rcx
  __int64 v90; // rax
  __int64 v91; // rax
  __int128 *v92; // rsi
  __int64 v93; // rbp
  _DWORD *v94; // r13
  unsigned __int64 v95; // rbx
  __int64 v96; // rdi
  __int128 *v97; // r15
  int v98; // r14d
  unsigned __int64 v99; // rax
  unsigned __int64 v100; // rsi
  char *v101; // r12
  __int64 v102; // r13
  unsigned __int64 v103; // rbp
  __int64 v104; // rdi
  _QWORD *v105; // rax
  __int64 v106; // rdi
  _QWORD *v107; // rbx
  __int64 v108; // r13
  unsigned __int64 v109; // rbp
  unsigned __int64 v110; // rdi
  _QWORD *v111; // rsi
  unsigned __int64 v112; // rsi
  __int64 v113; // rdi
  _DWORD *v114; // rcx
  unsigned __int64 v115; // rdi
  unsigned __int64 v116; // rsi
  __int64 v117; // rbp
  unsigned __int64 v118; // rdx
  __int64 v119; // rdi
  unsigned __int64 v120; // rsi
  _QWORD *v121; // rax
  __int64 v122; // rsi
  __int64 v123; // rax
  char v124; // al
  __int64 v125; // rax
  __int64 v126; // r13
  __int64 v127; // rax
  __int64 v128; // r12
  int v129; // edi
  __int64 v130; // rbx
  __int64 v131; // r15
  unsigned __int64 v132; // rax
  unsigned __int64 v133; // rsi
  unsigned __int64 v134; // rbp
  __int64 v135; // r14
  __int64 v136; // rdi
  __int64 v137; // rax
  unsigned __int64 v138; // rbp
  __int64 v139; // rbx
  int v140; // esi
  __int64 v141; // rbx
  __int64 v142; // rdx
  BOOL v143; // r14d
  _QWORD *v144; // rdi
  _QWORD *v145; // rax
  int v146; // ecx
  __int64 *v147; // rdx
  __int64 v148; // rax
  _QWORD *v149; // r12
  _QWORD *v150; // rbx
  __int64 v151; // r14
  __int64 v152; // r15
  unsigned __int64 v153; // rdi
  unsigned __int64 v154; // rbp
  unsigned __int64 v155; // rsi
  __int64 v156; // rbx
  unsigned __int64 v157; // rsi
  unsigned __int64 v158; // rsi
  unsigned __int64 v159; // rbx
  __int64 v160; // rdx
  __int64 v161; // rsi
  __int64 v162; // r14
  __int64 *v163; // rcx
  __int64 v164; // rax
  unsigned __int64 v165; // rdi
  __int64 *v166; // rcx
  __int64 v167; // rsi
  int v168; // ebp
  __int64 v169; // rbx
  __int64 v170; // rdx
  BOOL v171; // r15d
  _QWORD *v172; // rsi
  _QWORD *v173; // rax
  int v174; // ecx
  __int64 *v175; // rdx
  __int64 v176; // rax
  _DWORD *v177; // rsi
  __int64 *v178; // r14
  __int64 *v179; // rbp
  _QWORD *v180; // r12
  _QWORD *v181; // rbx
  __int64 v182; // r14
  __int64 v183; // r15
  unsigned __int64 v184; // rdi
  unsigned __int64 v185; // rbp
  unsigned __int64 v186; // rsi
  __int64 v187; // rbx
  unsigned __int64 v188; // rsi
  int v189; // r13d
  __int64 *v190; // rcx
  char *v191; // rbx
  unsigned __int64 v192; // rax
  unsigned __int64 v193; // r12
  unsigned __int64 v194; // rdi
  __int64 v195; // r15
  _DWORD *v196; // r13
  __int64 *v197; // rax
  __int64 *v198; // rcx
  unsigned __int64 v199; // rsi
  unsigned __int64 v200; // rbx
  __int64 v201; // rdx
  __int64 v202; // rsi
  __int64 v203; // r13
  _DWORD *v204; // r15
  _DWORD *v205; // r14
  unsigned __int64 v206; // rbx
  __int64 v207; // rax
  int v208; // esi
  __int64 v209; // r15
  unsigned __int64 v210; // r14
  unsigned __int64 v211; // rdi
  unsigned __int64 v212; // rcx
  unsigned __int64 v213; // rdi
  __int64 v214; // rbp
  _QWORD *v215; // rbx
  __int64 v216; // r14
  unsigned __int64 v217; // rbp
  unsigned __int64 v218; // rdi
  _QWORD *v219; // rsi
  unsigned __int64 v220; // rsi
  __int64 v221; // rdi
  unsigned __int64 v222; // rsi
  unsigned __int64 v223; // rdi
  unsigned __int64 v224; // rdx
  __int64 v225; // rsi
  unsigned __int64 v226; // rsi
  _DWORD *v227; // rsi
  _DWORD *v228; // r12
  unsigned __int64 v229; // rbp
  __int64 v230; // rax
  int v231; // ebx
  __int64 v232; // rsi
  unsigned __int64 v233; // rax
  unsigned __int64 v234; // r15
  __int64 v235; // r12
  unsigned __int64 v236; // rsi
  unsigned __int64 v237; // rcx
  unsigned __int64 v238; // rsi
  __int64 v239; // rdi
  _QWORD *v240; // r15
  __int64 v241; // r12
  unsigned __int64 v242; // rbp
  unsigned __int64 v243; // rsi
  _QWORD *v244; // rdi
  unsigned __int64 v245; // rbx
  __int64 v246; // rdi
  unsigned __int64 v247; // rdi
  unsigned __int64 v248; // rsi
  unsigned __int64 v249; // rdx
  __int64 v250; // rdi
  unsigned __int64 v251; // rsi
  __int64 v252; // r13
  _DWORD *v253; // r12
  _DWORD *v254; // r15
  unsigned __int64 v255; // rbp
  __int64 v256; // rax
  int v257; // r14d
  __int64 v258; // r12
  unsigned __int64 v259; // rsi
  unsigned __int64 v260; // rbx
  unsigned __int64 v261; // rcx
  unsigned __int64 v262; // rbx
  __int64 v263; // rdi
  _QWORD *v264; // rbp
  __int64 v265; // r15
  unsigned __int64 v266; // rsi
  unsigned __int64 v267; // rdi
  _QWORD *v268; // rbx
  unsigned __int64 v269; // rbx
  __int64 v270; // rdi
  unsigned __int64 v271; // rsi
  unsigned __int64 v272; // rdi
  unsigned __int64 v273; // rbx
  unsigned __int64 v274; // rdx
  __int64 v275; // rdi
  __int64 v276; // rax
  __int64 v277; // rax
  __int64 v278; // rax
  __int64 v279; // rax
  int v280; // esi
  int v281; // eax
  __int64 v282; // rcx
  int v283; // r8d
  __int64 v284; // rcx
  __int64 v285; // rcx
  __int64 v286; // rdx
  __int64 v287; // r8
  _QWORD *v288; // rdi
  void (__fastcall ***v289)(_QWORD, __int64); // rcx
  void (__fastcall ***v290)(_QWORD, __int64); // rcx
  __int64 v291; // rsi
  void (__fastcall ***v292)(_QWORD, __int64); // rcx
  _QWORD *v293; // rax
  __int64 v294; // rsi
  volatile signed __int32 *v295; // rcx
  int v297; // [rsp+20h] [rbp-3B8h]
  int v298; // [rsp+20h] [rbp-3B8h]
  int v299; // [rsp+20h] [rbp-3B8h]
  int v300; // [rsp+20h] [rbp-3B8h]
  int v301; // [rsp+20h] [rbp-3B8h]
  int v302; // [rsp+20h] [rbp-3B8h]
  int v303; // [rsp+20h] [rbp-3B8h]
  int v304; // [rsp+20h] [rbp-3B8h]
  int v305; // [rsp+20h] [rbp-3B8h]
  int v306; // [rsp+20h] [rbp-3B8h]
  int v307; // [rsp+20h] [rbp-3B8h]
  int v308; // [rsp+20h] [rbp-3B8h]
  __int64 v309; // [rsp+68h] [rbp-370h]
  __int64 v310; // [rsp+68h] [rbp-370h]
  __int128 v311; // [rsp+70h] [rbp-368h] BYREF
  _DWORD *v312; // [rsp+80h] [rbp-358h]
  __int64 v313; // [rsp+88h] [rbp-350h] BYREF
  __int64 v314; // [rsp+90h] [rbp-348h]
  _DWORD *v315; // [rsp+98h] [rbp-340h]
  _QWORD *v316; // [rsp+A0h] [rbp-338h] BYREF
  BOOL v317; // [rsp+A8h] [rbp-330h]
  __int128 v318; // [rsp+B0h] [rbp-328h] BYREF
  __int64 v319; // [rsp+C0h] [rbp-318h]
  __int64 v320; // [rsp+C8h] [rbp-310h] BYREF
  int v321; // [rsp+D0h] [rbp-308h] BYREF
  __int64 v322; // [rsp+D8h] [rbp-300h] BYREF
  char v323[8]; // [rsp+E0h] [rbp-2F8h] BYREF
  volatile signed __int32 *v324; // [rsp+E8h] [rbp-2F0h] BYREF
  __int128 v325; // [rsp+F0h] [rbp-2E8h] BYREF
  __int64 v326; // [rsp+100h] [rbp-2D8h]
  __int128 v327; // [rsp+110h] [rbp-2C8h] BYREF
  __int64 v328; // [rsp+120h] [rbp-2B8h]
  int v329; // [rsp+130h] [rbp-2A8h] BYREF
  int v330; // [rsp+138h] [rbp-2A0h] BYREF
  int v331; // [rsp+140h] [rbp-298h] BYREF
  int v332; // [rsp+148h] [rbp-290h] BYREF
  int v333; // [rsp+150h] [rbp-288h] BYREF
  __int64 v334; // [rsp+158h] [rbp-280h] BYREF
  __int64 v335; // [rsp+160h] [rbp-278h] BYREF
  volatile signed __int32 *v336[2]; // [rsp+168h] [rbp-270h] BYREF
  char v337; // [rsp+178h] [rbp-260h]
  char v338; // [rsp+1C4h] [rbp-214h]
  __int64 v339; // [rsp+1C8h] [rbp-210h]
  __int64 v340; // [rsp+1D0h] [rbp-208h]
  __int64 v341; // [rsp+1D8h] [rbp-200h]
  __int64 v342; // [rsp+1E0h] [rbp-1F8h]
  __int64 *v343; // [rsp+1E8h] [rbp-1F0h]
  __int64 v344; // [rsp+1F0h] [rbp-1E8h]
  __int64 v345; // [rsp+1F8h] [rbp-1E0h]
  __int64 v346; // [rsp+200h] [rbp-1D8h]
  char v347; // [rsp+208h] [rbp-1D0h]
  __int64 v348; // [rsp+210h] [rbp-1C8h]
  __int64 v349; // [rsp+218h] [rbp-1C0h]
  _QWORD *v350; // [rsp+220h] [rbp-1B8h]
  __int64 v351; // [rsp+228h] [rbp-1B0h]
  __int64 v352; // [rsp+230h] [rbp-1A8h]
  __int64 v353; // [rsp+238h] [rbp-1A0h]
  __int64 v354; // [rsp+240h] [rbp-198h]
  __int64 v355; // [rsp+248h] [rbp-190h]
  __int64 v356; // [rsp+250h] [rbp-188h]
  __int64 v357; // [rsp+258h] [rbp-180h]
  _DWORD *v358; // [rsp+260h] [rbp-178h]
  __int64 v359; // [rsp+268h] [rbp-170h]
  _DWORD *v360; // [rsp+270h] [rbp-168h]
  __int64 v361; // [rsp+278h] [rbp-160h]
  _QWORD v362[2]; // [rsp+280h] [rbp-158h] BYREF
  __int64 v363; // [rsp+290h] [rbp-148h]
  __int64 v364; // [rsp+2A0h] [rbp-138h]
  _QWORD v365[2]; // [rsp+2B0h] [rbp-128h] BYREF
  __int64 v366; // [rsp+2C0h] [rbp-118h]
  _QWORD v367[2]; // [rsp+2D0h] [rbp-108h] BYREF
  __int64 v368; // [rsp+2E0h] [rbp-F8h]
  _QWORD v369[2]; // [rsp+300h] [rbp-D8h] BYREF
  __int64 v370; // [rsp+310h] [rbp-C8h]
  __int64 v371; // [rsp+320h] [rbp-B8h]
  __int64 v372; // [rsp+330h] [rbp-A8h]
  __int64 v373; // [rsp+338h] [rbp-A0h]
  __int64 v374; // [rsp+340h] [rbp-98h]
  __int64 v375; // [rsp+350h] [rbp-88h]
  __int64 v376; // [rsp+358h] [rbp-80h]
  __int64 v377; // [rsp+360h] [rbp-78h]

  LOBYTE(v2) = 1;
  if ( a2 != 0 )
    return (unsigned int)v2;
  BYTE4(qword_141B5E498) &= ~1u;
  v4 = qword_141ABDFE8;
  LODWORD(v2) = 0;
  sub_14083D6D0(a1: v336, a2: 0);
  v5 = sub_140800A10(a1: v4, a2: &unk_141ABFC88, a3: v336, a4: 0);
  sub_14083D320(a1: v336);
  LOBYTE(v6) = 1;
  if ( (unsigned __int8)sub_14000F400(
                          a1,
                          a2: 0,
                          a3: v6,
                          a4: 0,
                          a5: 0,
                          a6: 0,
                          a7: 1,
                          a8: (__int64)&qword_141B59EE0,
                          a9: (__int64)&qword_141B59EE0,
                          a10: 1,
                          a11: v5,
                          a12: 0) == 0 )
    return (unsigned int)v2;
  LOBYTE(word_141B60460) = 2;
  v336[0] = nullptr;
  sub_1407D5DC0(a1: qword_141ABD878, a2: v362, a3: &qword_141B5ACC0);
  sub_1407C3450(a1: &v324, a2: v362, a3: v336);
  v7 = (void (__fastcall ***)(_QWORD, __int64))v362[0];
  if ( v362[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v362[0] + 8LL)) == 0 )
    (**v7)(a1: v7, a2: 1);
  v8 = v336[0];
  if ( v336[0] != nullptr && _InterlockedDecrement(v336[0]) == 0 )
  {
    sub_140053440(a1: v8 + 2, a2: v8 + 2, a3: *(_QWORD *)(*((_QWORD *)v8 + 1) + 8LL));
    sub_1407E4890(a1: qword_141ABD470, a2: *((_QWORD *)v8 + 1), a3: 48);
    sub_141750CFC(a1: v8);
  }
  if ( v324 == nullptr )
  {
    LODWORD(v2) = 0;
    return (unsigned int)v2;
  }
  v334 = 0;
  sub_140809100(a1: &v334, a2: &qword_141B60338);
  v9 = v324;
  sub_1407D5F40(a1: v336, a2: &v334);
  sub_1407D2430(a1: v9, a2: &v313, a3: v336);
  sub_140808B00(a1: v336);
  if ( v313 != 0 )
  {
    sub_1407D8AB0(a1: v336, a2: 0x1418E2C24LL);
    sub_1407D5F40(a1: v362, a2: &qword_141B5ACD8);
    LOBYTE(v297) = 1;
    sub_1400015E0(a1, a2: &v313, a3: v362, a4: v336, a5: v297);
    sub_140808B00(a1: v362);
    sub_1407D8AB0(a1: v336, a2: 0x1418E2C24LL);
    sub_1407D5F40(a1: v362, a2: &qword_141B5ACE0);
    LOBYTE(v298) = 1;
    sub_1400015E0(a1, a2: &v313, a3: v362, a4: v336, a5: v298);
    sub_140808B00(a1: v362);
    sub_1407D8AB0(a1: v336, a2: 0x1418E2C24LL);
    sub_1407D5F40(a1: v362, a2: &qword_141ABD940);
    LOBYTE(v299) = 1;
    sub_1400015E0(a1, a2: &v313, a3: v362, a4: v336, a5: v299);
    sub_140808B00(a1: v362);
    sub_1407D8AB0(a1: v336, a2: 0x1418E2C24LL);
    sub_1407D5F40(a1: v362, a2: &qword_141B5ACE8);
    LOBYTE(v300) = 1;
    sub_1400015E0(a1, a2: &v313, a3: v362, a4: v336, a5: v300);
    sub_140808B00(a1: v362);
    sub_1407D8AB0(a1: v336, a2: 0x1418E2C24LL);
    sub_1407D5F40(a1: v362, a2: &qword_141ABD930);
    LOBYTE(v301) = 1;
    sub_1400015E0(a1, a2: &v313, a3: v362, a4: v336, a5: v301);
    sub_140808B00(a1: v362);
    sub_1407D8AB0(a1: v336, a2: 0x1418E2C24LL);
    sub_1407D5F40(a1: v362, a2: &qword_141ABD938);
    LOBYTE(v302) = 1;
    sub_1400015E0(a1, a2: &v313, a3: v362, a4: v336, a5: v302);
    sub_140808B00(a1: v362);
    v10 = v313;
    sub_1407D8AB0(a1: v336, a2: 0x1418E2C24LL);
    sub_1407D5F40(a1: v362, a2: &qword_141B5ACD8);
    sub_1407D2460(a1: v10, a2: (unsigned int)&v321, a3: (unsigned int)v362, a4: (unsigned int)v336, a5: 3);
    if ( v321 != 0 )
    {
LABEL_14:
      sub_140808B00(a1: v362);
      goto LABEL_15;
    }
    v11 = v313;
    sub_1407D8AB0(a1: v369, a2: 0x1418E2C24LL);
    sub_1407D5F40(a1: &v327, a2: &qword_141B5ACE0);
    sub_1407D2460(a1: v11, a2: (unsigned int)&v333, a3: (unsigned int)&v327, a4: (unsigned int)v369, a5: 3);
    if ( v333 != 0 )
    {
      sub_140808B00(a1: &v327);
      goto LABEL_14;
    }
    v17 = v313;
    sub_1407D8AB0(a1: &v325, a2: 0x1418E2C24LL);
    sub_1407D5F40(a1: &v311, a2: &qword_141ABD940);
    sub_1407D2460(a1: v17, a2: (unsigned int)&v332, a3: (unsigned int)&v311, a4: (unsigned int)&v325, a5: 3);
    if ( v332 != 0 )
    {
      v18 = true;
    }
    else
    {
      v19 = v313;
      sub_1407D8AB0(a1: &v316, a2: 0x1418E2C24LL);
      sub_1407D5F40(a1: &v318, a2: &qword_141B5ACE8);
      sub_1407D2460(a1: v19, a2: (unsigned int)&v331, a3: (unsigned int)&v318, a4: (unsigned int)&v316, a5: 3);
      if ( v331 != 0 )
      {
        v18 = true;
      }
      else
      {
        v20 = v313;
        sub_1407D8AB0(a1: &v320, a2: 0x1418E2C24LL);
        sub_1407D5F40(a1: v323, a2: &qword_141ABD930);
        sub_1407D2460(a1: v20, a2: (unsigned int)&v330, a3: (unsigned int)v323, a4: (unsigned int)&v320, a5: 3);
        if ( v330 != 0 )
        {
          v18 = true;
        }
        else
        {
          v21 = v313;
          sub_1407D8AB0(a1: &v322, a2: 0x1418E2C24LL);
          sub_1407D5F40(a1: &v335, a2: &qword_141ABD938);
          sub_1407D2460(a1: v21, a2: (unsigned int)&v329, a3: (unsigned int)&v335, a4: (unsigned int)&v322, a5: 3);
          v18 = v329 != 0;
          sub_140808B00(a1: &v335);
        }
        sub_140808B00(a1: v323);
      }
      sub_140808B00(a1: &v318);
    }
    sub_140808B00(a1: &v311);
    sub_140808B00(a1: &v327);
    sub_140808B00(a1: v362);
    if ( v18 )
    {
LABEL_15:
      LODWORD(v2) = 0;
      if ( (dword_141ABD994 & 1) != 0 && dword_141ABD990 <= 1 )
      {
        v12 = &unk_141ABD978;
        while ( 1 )
        {
          v12 = (_QWORD *)v12[2];
          if ( v12 == nullptr || *v12 == 0 )
            break;
          if ( (*((_BYTE *)v12 + 28) & 1) == 0 || *((int *)v12 + 6) > 1 )
            goto LABEL_424;
        }
        v13 = sub_1407E2C90(a1: 2160);
        sub_1407E2EB0(a1: v13, a2: 1099914335, a3: 19799, a4: 1099882446, a5: 0, a6: 1);
        v14 = sub_1407E0010(a1: v13, a2: 0x1419401EELL);
        (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)v324 + 32LL))(
          a1: v324,
          a2: v336);
        sub_1407D6070(a1: v14, a2: v336);
        sub_140808B00(a1: v336);
        if ( (sub_1407E0380(a1: &unk_141ABD978, a2: v13) & 4) != 0 )
        {
          sub_1407CD750(a1: v15);
          LODWORD(v2) = 0;
          v16 = v313;
          if ( v313 == 0 )
            goto LABEL_425;
LABEL_408:
          if ( _InterlockedDecrement((volatile signed __int32 *)(v16 + 8)) == 0 )
            (**(void (__fastcall ***)(__int64, __int64))v16)(a1: v16, a2: 1);
          goto LABEL_425;
        }
        goto LABEL_424;
      }
LABEL_407:
      v16 = v313;
      if ( v313 != 0 )
        goto LABEL_408;
      goto LABEL_425;
    }
  }
  v22 = qword_141ABD830;
  *(_WORD *)(qword_141ABD830 + 1347) = 256;
  v23 = *(_QWORD *)(qword_141B5AD60 + 24);
  v349 = *(_QWORD *)(qword_141B5AD60 + 16);
  v348 = v23;
  if ( v23 != v349 )
    goto LABEL_56;
  v336[0] = nullptr;
  nullsub_1(a1: qword_141B5AD60, a2: v336);
  v26 = v336[0];
  if ( v336[0] != nullptr && _InterlockedDecrement(v336[0] + 2) == 0 )
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v26)(a1: v26, a2: 1);
  v27 = *(_QWORD *)(qword_141ABF5C0 + 44424);
  if ( *(_QWORD *)(qword_141ABF5C0 + 44432) != v27 )
  {
    v28 = 0;
    do
    {
      v29 = (volatile signed __int32 *)sub_14083E160(a1: *(_QWORD *)(v27 + 8 * v28));
      v336[0] = (volatile signed __int32 *)0x14175CD28LL;
      v336[1] = v29;
      v337 = 1;
      if ( (unsigned __int8)sub_140CD9140(a1: v336, a2: v362) == 0 || LOBYTE(v362[0]) == 0 )
      {
        sub_140833AD0(a1: v336, a2: v29);
        sub_1408916D0(
          a1: qword_141B5AD60,
          a2: (unsigned int)v336,
          a3: 0,
          a4: 0,
          a5: (__int64)&qword_141B5A4A0,
          a6: (__int64)&qword_141B5A458,
          a7: 0,
          a8: 0);
        sub_140833970(a1: v336);
      }
      ++v28;
      v27 = *(_QWORD *)(qword_141ABF5C0 + 44424);
    }
    while ( v28 < (*(_QWORD *)(qword_141ABF5C0 + 44432) - v27) >> 3 );
  }
  LOBYTE(v24) = 1;
  LOBYTE(v25) = 1;
  (*(void (__fastcall **)(__int64, _QWORD, __int64, __int64))(*(_QWORD *)qword_141B5AD60 + 600LL))(
    a1: qword_141B5AD60,
    a2: 0,
    a3: v24,
    a4: v25);
  sub_14083D2C0(a1: v362);
  if ( (unsigned __int8)sub_140800D80(a1: qword_141ABDFE8, a2: &unk_141ABFCB0, a3: v362) == 0
    || (v30 = *(_QWORD *)(qword_141B5AD60 + 16), (v31 = *(_QWORD *)(qword_141B5AD60 + 24) - v30) == 0) )
  {
LABEL_55:
    sub_14083D320(a1: v362);
    v22 = qword_141ABD830;
LABEL_56:
    *(_BYTE *)(v22 + 1347) = 1;
    v36 = 0;
    sub_140F5AA50(a1: &qword_141B5FDA8, a2: 0);
    v320 = 0;
    v37 = (_QWORD *)qword_141B5AD60;
    v336[0] = nullptr;
    sub_140809040(a1: v336, a2: 0x14192D50DLL, a3: 0xFFFFFFFFLL);
    sub_1408B1260(
      a1: (_DWORD)v37,
      a2: (unsigned int)v336,
      a3: (unsigned int)&qword_141B59EE0,
      a4: (unsigned int)&qword_141B59EE0,
      a5: (__int64)v323,
      a6: -1,
      a7: 0,
      a8: 0,
      a9: 0,
      a10: 0,
      a11: 0);
    sub_140808B00(a1: v336);
    sub_140F5B9D0(a1: (unsigned int)v362, a2: (unsigned __int8)byte_141B60462, a3: 0, a4: 0, a5: 2);
    v38 = sub_1404377F0(a1: &qword_141B5FDA8);
    sub_140F5C8A0(
      a1: (unsigned int)&qword_141B5FDA8,
      a2: v38,
      a3: 0,
      a4: 0,
      a5: 0,
      a6: (__int64)v362,
      a7: (__int64)&v320,
      a8: (__int64)&v320,
      a9: 0,
      a10: 300);
    sub_140F75CF0(a1: &qword_141B5FDA8);
    sub_1407D5DC0(a1: qword_141ABD878, a2: &v322, a3: &qword_141B5EDF0);
    v40 = qword_141B60400 - qword_141B603F8;
    v327 = 0;
    v328 = 0;
    v41 = 0;
    v42 = qword_141B60400 - qword_141B603F8;
    if ( qword_141B60400 != qword_141B603F8 )
    {
      if ( qword_141B60400 - qword_141B603F8 < 0 )
LABEL_430:
        sub_1400526C0(a1: v39, a2: v42);
      v43 = sub_1407E4490(a1: qword_141ABD470, a2: v42);
      *(_QWORD *)&v327 = v43;
      *((_QWORD *)&v327 + 1) = v43;
      v328 = v43 + 4 * (v40 >> 2);
      v44 = qword_141B60400 - qword_141B603F8;
      sub_141758A00(a1: v43, a2: qword_141B603F8, a3: qword_141B60400 - qword_141B603F8);
      v41 = v43 + v44;
      *((_QWORD *)&v327 + 1) = v41;
      v36 = v327;
    }
    sub_140057690(a1: v36, a2: v41, a3: (v41 - v36) >> 2);
    if ( qword_141ABD470 == 0 )
      qword_141ABD470 = sub_1407E4940();
    v325 = 0;
    v326 = 0;
    sub_140885620(a1: &v325);
    sub_14011BE90(
      a1,
      a2: 0,
      a3: (*((_QWORD *)&v325 + 1) - (_QWORD)v325) >> 3,
      a4: 0,
      a5: (__int64)&qword_141B59EE0,
      a6: 0);
    v45 = v325;
    if ( *((_QWORD *)&v325 + 1) == (_QWORD)v325 )
    {
LABEL_383:
      sub_14011C160(a1);
      v280 = qword_141B5AD60;
      v336[0] = nullptr;
      sub_140809040(a1: v336, a2: 0x14192D50DLL, a3: 0xFFFFFFFFLL);
      sub_1408B1260(
        a1: v280,
        a2: (unsigned int)v336,
        a3: (unsigned int)&qword_141B59EE0,
        a4: (unsigned int)&qword_141B59EE0,
        a5: (__int64)v323,
        a6: -1,
        a7: 0,
        a8: 0,
        a9: 0,
        a10: 0,
        a11: 1);
      sub_140808B00(a1: v336);
      v281 = sub_1404377F0(a1: &qword_141B5FDA8);
      sub_140F5C8A0(
        a1: (unsigned int)&qword_141B5FDA8,
        a2: v281,
        a3: 0,
        a4: 0,
        a5: 0,
        a6: (__int64)v362,
        a7: (__int64)&v320,
        a8: (__int64)&v320,
        a9: 0,
        a10: 300);
      LOWORD(v282) = 128;
      sub_140F62A50(a1: v282);
      while ( (unsigned __int8)sub_140F62A70() == 0 )
      {
        LOBYTE(v336[0]) = 0;
        LOBYTE(v283) = 1;
        sub_140F64530(
          a1: (unsigned int)&qword_141B5FDA8,
          a2: (unsigned int)&v322,
          a3: v283,
          a4: (unsigned int)v336,
          a5: 1,
          a6: 0,
          a7: 0);
      }
      sub_1400977F0(a1: qword_141ABD830, a2: &qword_141B5ACD8, a3: a1 + 44656, a4: &v334);
      sub_1400977F0(a1: qword_141ABD830, a2: &qword_141B5ACE0, a3: a1 + 44672, a4: &v334);
      sub_1400977F0(a1: qword_141ABD830, a2: &qword_141B5ACE8, a3: a1 + 44688, a4: &v334);
      sub_1400977F0(a1: qword_141ABD830, a2: &qword_141ABD938, a3: a1 + 44720, a4: &v334);
      sub_1400977F0(a1: qword_141ABD830, a2: &qword_141ABD930, a3: a1 + 44704, a4: &v334);
      sub_1400977F0(a1: qword_141ABD830, a2: &qword_141ABD940, a3: a1 + 44736, a4: &v334);
      sub_1407D8AB0(a1: v336, a2: 0x1418E2C24LL);
      sub_1407D5F40(a1: v369, a2: &qword_141B5ACD8);
      sub_1400015E0(a1, a2: &v313, a3: v369, a4: v336, a5: v303);
      sub_140808B00(a1: v369);
      sub_1407D8AB0(a1: v336, a2: 0x1418E2C24LL);
      sub_1407D5F40(a1: v369, a2: &qword_141B5ACE0);
      sub_1400015E0(a1, a2: &v313, a3: v369, a4: v336, a5: v304);
      sub_140808B00(a1: v369);
      sub_1407D8AB0(a1: v336, a2: 0x1418E2C24LL);
      sub_1407D5F40(a1: v369, a2: &qword_141ABD940);
      sub_1400015E0(a1, a2: &v313, a3: v369, a4: v336, a5: v305);
      sub_140808B00(a1: v369);
      sub_1407D8AB0(a1: v336, a2: 0x1418E2C24LL);
      sub_1407D5F40(a1: v369, a2: &qword_141B5ACE8);
      sub_1400015E0(a1, a2: &v313, a3: v369, a4: v336, a5: v306);
      sub_140808B00(a1: v369);
      sub_1407D8AB0(a1: v336, a2: 0x1418E2C24LL);
      sub_1407D5F40(a1: v369, a2: &qword_141ABD930);
      sub_1400015E0(a1, a2: &v313, a3: v369, a4: v336, a5: v307);
      sub_140808B00(a1: v369);
      sub_1407D8AB0(a1: v336, a2: 0x1418E2C24LL);
      sub_1407D5F40(a1: v369, a2: &qword_141ABD938);
      sub_1400015E0(a1, a2: &v313, a3: v369, a4: v336, a5: v308);
      sub_140808B00(a1: v369);
      sub_14003C880(a1: v284, a2: &v334);
      sub_14004E450(a1: v285, a2: a1 + 44656);
      sub_1400977F0(a1: qword_141ABD830, a2: &qword_141B5ACD8, a3: a1 + 44656, a4: &v334);
      LOBYTE(v286) = 2;
      LOBYTE(v287) = 1;
      sub_140048920(a1, a2: v286, a3: v287, a4: 0);
      if ( v348 == v349 )
        (*(void (__fastcall **)(__int64))(*(_QWORD *)qword_141B5AD60 + 760LL))(a1: qword_141B5AD60);
      LOBYTE(word_141B60460) = 6;
      v2 = (_QWORD *)v325;
      if ( (_QWORD)v325 != 0 )
      {
        v288 = *((_QWORD **)&v325 + 1);
        if ( (_QWORD)v325 != *((_QWORD *)&v325 + 1) )
        {
          do
            sub_140808B00(a1: v2++);
          while ( v2 != v288 );
          v2 = (_QWORD *)v325;
        }
        sub_1407E4890(a1: qword_141ABD470, a2: v2, a3: v326 - (_QWORD)v2);
      }
      if ( (_QWORD)v327 != 0 )
        sub_1407E4890(a1: qword_141ABD470, a2: v327, a3: v328 - v327);
      v289 = (void (__fastcall ***)(_QWORD, __int64))v322;
      if ( v322 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v322 + 8)) == 0 )
        (**v289)(a1: v289, a2: 1);
      if ( v367[0] != 0 )
      {
        v2 = v367;
        sub_1407E4890(a1: qword_141ABD470, a2: v367[0], a3: v368 - v367[0]);
        v368 = 0;
        v367[1] = 0;
        v367[0] = 0;
      }
      if ( v365[0] != 0 )
      {
        v2 = v365;
        sub_1407E4890(a1: qword_141ABD470, a2: v365[0], a3: v366 - v365[0]);
        v366 = 0;
        v365[1] = 0;
        v365[0] = 0;
      }
      if ( v363 != 0 )
        sub_1407E4890(a1: qword_141ABD470, a2: v363, a3: v364 - v363);
      v290 = (void (__fastcall ***)(_QWORD, __int64))v320;
      if ( v320 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v320 + 16)) == 0 )
        (**v290)(a1: v290, a2: 1);
      LOBYTE(v2) = 1;
      goto LABEL_407;
    }
    v357 = a1 + 44656;
    v356 = a1 + 44672;
    v355 = a1 + 44688;
    v354 = a1 + 44704;
    v353 = a1 + 44720;
    v352 = a1 + 44736;
    v46 = 0;
    v351 = a1;
    v350 = v37;
    while ( 1 )
    {
      v361 = v46;
      v314 = v45 + 8 * v46;
      sub_1408B1260(
        a1: (_DWORD)v37,
        a2: v314,
        a3: (unsigned int)&qword_141B59EE0,
        a4: (unsigned int)&qword_141B59EE0,
        a5: (__int64)v323,
        a6: -1,
        a7: 0,
        a8: 0,
        a9: 1,
        a10: 0,
        a11: 1);
      sub_1408A1C30(a1: v37, a2: 0);
      sub_1408A1AC0(a1: v37);
      LOBYTE(v47) = 1;
      LOBYTE(v48) = 1;
      sub_14088EF20(a1: v37, a2: v47, a3: v48);
      v49 = v37[2];
      v50 = v37[3];
      if ( v50 != v49 )
      {
        v51 = 0;
        do
        {
          v52 = *(_QWORD *)(v49 + 8 * v51);
          if ( *(_BYTE *)(v52 + 68) != 0 )
          {
            sub_14087E950(a1: v52, a2: v37[9]);
            v49 = v37[2];
            v50 = v37[3];
          }
          ++v51;
        }
        while ( v51 < (v50 - v49) >> 3 );
      }
      sub_140F5B9D0(a1: (unsigned int)v369, a2: (unsigned __int8)byte_141B60462, a3: 0, a4: 0, a5: 2);
      v53 = sub_1404377F0(a1: &qword_141B5FDA8);
      sub_140F5C8A0(
        a1: (unsigned int)&qword_141B5FDA8,
        a2: v53,
        a3: 0,
        a4: 0,
        a5: 0,
        a6: (__int64)v369,
        a7: (__int64)&v320,
        a8: (__int64)&v320,
        a9: 0,
        a10: 300);
      sub_140FFA310(a1: v336, a2: 1, a3: 0);
      v336[0] = (volatile signed __int32 *)0x14175D368LL;
      if ( qword_141ABD470 == 0 )
        qword_141ABD470 = sub_1407E4940();
      v342 = 0;
      v341 = 0;
      v340 = 0;
      v339 = 0;
      v54 = sub_1407E4940();
      v56 = (__int64 *)sub_1407E4490(a1: v54, a2: 24);
      if ( qword_141ABD470 == 0 )
        qword_141ABD470 = sub_1407E4940();
      v56[2] = 0;
      v56[1] = 0;
      *v56 = 0;
      v343 = v56;
      v347 = 0;
      v346 = 0;
      v345 = 0;
      v344 = 0;
      LOWORD(v55) = 128;
      sub_140F62A50(a1: v55);
      while ( (unsigned __int8)sub_140F62A70() == 0 )
      {
        LOBYTE(v311) = 0;
        LOBYTE(v57) = 1;
        sub_140F64530(
          a1: (unsigned int)&qword_141B5FDA8,
          a2: (unsigned int)&v322,
          a3: v57,
          a4: (unsigned int)&v311,
          a5: 1,
          a6: 0,
          a7: (__int64)v336);
      }
      v309 = sub_140F90F70(a1: &qword_141B5FDA8);
      v58 = *(_QWORD *)(*(_QWORD *)(v309 + 128) + 8LL) - **(_QWORD **)(v309 + 128);
      if ( v58 != 0 )
      {
        v59 = v58 >> 3;
        if ( v59 < 2 )
          v59 = 1;
        for ( i = 0; i != v59; ++i )
        {
          v61 = *v343;
          v62 = v343[1];
          if ( *v343 == v62 )
            continue;
          v63 = *(_QWORD *)(**(_QWORD **)(v309 + 128) + 8 * i);
          v64 = *(_DWORD *)(v63 + 24);
          if ( v64 <= 0 )
            continue;
          if ( (v338 & 1) != 0 )
          {
            if ( v347 != 0 )
            {
              sub_140054D70(a1: v344, a2: v345, a3: (v345 - v344) >> 3, a4: sub_1400115D0);
              v347 = 0;
            }
            v71 = (unsigned __int64)(v345 - v344) >> 3;
            if ( (int)v71 <= 0 )
            {
LABEL_99:
              v75 = 0;
              if ( *(int *)(v63 + 28) > 0 )
                goto LABEL_100;
              goto LABEL_127;
            }
            v72 = v71 - 1;
            v73 = 0;
            while ( 1 )
            {
              while ( 1 )
              {
                v74 = (unsigned int)(v73 + v72) >> 1;
                v69 = *(_QWORD *)(v344 + 8 * v74);
                v70 = *(_DWORD *)(v69 + 12);
                if ( v70 <= v64 )
                  break;
                v72 = v74 - 1;
                if ( v73 > (int)v74 - 1 )
                  goto LABEL_99;
              }
              if ( v70 >= v64 )
                break;
              v73 = v74 + 1;
              if ( (int)v74 + 1 > v72 )
                goto LABEL_99;
            }
          }
          else
          {
            v65 = (unsigned __int64)(v62 - v61) >> 3;
            if ( (int)v65 <= 0 )
              goto LABEL_99;
            v66 = v65 - 1;
            v67 = 0;
            while ( 1 )
            {
              while ( 1 )
              {
                v68 = (unsigned int)(v67 + v66) >> 1;
                v69 = *(_QWORD *)(v61 + 8 * v68);
                v70 = *(_DWORD *)(v69 + 12);
                if ( v70 <= v64 )
                  break;
                v66 = v68 - 1;
                if ( v67 > (int)v68 - 1 )
                  goto LABEL_99;
              }
              if ( v70 >= v64 )
                break;
              v67 = v68 + 1;
              if ( (int)v68 + 1 > v66 )
                goto LABEL_99;
            }
          }
          v84 = *(_DWORD *)(v63 + 28);
          v85 = *(_DWORD *)(v69 + 16);
          if ( v85 == 0 )
            v85 = v70;
          if ( v85 == v84 || v84 == 0 && v85 == v70 )
            goto LABEL_128;
          if ( v84 != 0 )
            v69 = 0;
          v75 = v69;
          if ( v84 > 0 )
          {
LABEL_100:
            v76 = sub_140FFAA00(a1: v336, a2: (unsigned int)v64);
            if ( v76 != v64 )
            {
              v77 = v76;
              v78 = *v343;
              v79 = v343[1];
              if ( *v343 != v79 )
              {
                if ( (v338 & 1) != 0 )
                {
                  if ( v347 != 0 )
                  {
                    sub_140054D70(a1: v344, a2: v345, a3: (v345 - v344) >> 3, a4: sub_1400115D0);
                    v347 = 0;
                  }
                  v86 = (unsigned __int64)(v345 - v344) >> 3;
                  if ( (int)v86 > 0 )
                  {
                    v87 = v86 - 1;
                    v88 = 0;
                    do
                    {
                      while ( 1 )
                      {
                        v89 = (unsigned int)(v88 + v87) >> 1;
                        v69 = *(_QWORD *)(v344 + 8 * v89);
                        if ( *(_DWORD *)(v69 + 12) <= v77 )
                          break;
                        v87 = v89 - 1;
                        if ( v88 > (int)v89 - 1 )
                          goto LABEL_127;
                      }
                      if ( *(_DWORD *)(v69 + 12) >= v77 )
                        goto LABEL_128;
                      v88 = v89 + 1;
                    }
                    while ( (int)v89 + 1 <= v87 );
                  }
                }
                else
                {
                  v80 = (unsigned __int64)(v79 - v78) >> 3;
                  if ( (int)v80 > 0 )
                  {
                    v81 = v80 - 1;
                    v82 = 0;
                    while ( 1 )
                    {
                      while ( 1 )
                      {
                        v83 = (unsigned int)(v82 + v81) >> 1;
                        v69 = *(_QWORD *)(v78 + 8 * v83);
                        if ( *(_DWORD *)(v69 + 12) <= v77 )
                          break;
                        v81 = v83 - 1;
                        if ( v82 > (int)v83 - 1 )
                          goto LABEL_127;
                      }
                      if ( *(_DWORD *)(v69 + 12) >= v77 )
                        break;
                      v82 = v83 + 1;
                      if ( (int)v83 + 1 > v81 )
                        goto LABEL_127;
                    }
LABEL_128:
                    if ( *(unsigned __int16 *)(v63 + 34) <= 0x7E7u )
                    {
                      if ( (unsigned __int8)sub_14119E0D0(a1: v63) == 0
                        || (v90 = sub_14119E0B0(a1: v63),
                            (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v90 + 1304LL))(a1: v90) == 0)
                        && (unsigned __int8)sub_14119E0D0(a1: v63) != 0 )
                      {
                        *(_BYTE *)(v69 + 24) |= 0x40u;
                      }
                    }
                    continue;
                  }
                }
              }
            }
          }
LABEL_127:
          v69 = v75;
          if ( v75 != 0 )
            goto LABEL_128;
        }
      }
      sub_140F78600(
        a1: (unsigned int)&qword_141B5FDA8,
        a2: (unsigned int)&v321,
        a3: 0,
        a4: (unsigned int)v336,
        a5: (__int64)sub_1400526E0);
      if ( qword_141ABD470 == 0 )
        qword_141ABD470 = sub_1407E4940();
      v91 = *v343;
      v92 = &v327;
      if ( v343[1] == *v343 )
      {
        v93 = 0;
        v94 = nullptr;
        v315 = nullptr;
      }
      else
      {
        v93 = 0;
        v315 = nullptr;
        v94 = nullptr;
        v95 = 0;
        do
        {
          v96 = *(_QWORD *)(v91 + 8 * v95);
          if ( v96 != 0 && (unsigned __int8)sub_1400E4E60(a1: *(_QWORD *)(v91 + 8 * v95), a2: v369, a3: v92) == 1 )
          {
            v97 = v92;
            v98 = *(_DWORD *)(v96 + 12);
            if ( v94 == v315 )
            {
              v99 = ((__int64)v315 - v93) >> 2;
              v100 = v99 + 1;
              v101 = (char *)v315 - v93;
              v102 = v93;
              v103 = v99 + (v99 >> 1);
              if ( v103 <= v99 + 1 )
                v103 = v99 + 1;
              if ( v99 > 0x3FFFFFFFFFFFFFFFLL - (v99 >> 1) )
                v103 = 0x3FFFFFFFFFFFFFFFLL;
              v104 = sub_1407E4490(a1: qword_141ABD470, a2: 4 * v103);
              *(_DWORD *)&v101[v104] = v98;
              sub_141758A00(a1: v104, a2: v102, a3: v101);
              if ( v102 != 0 )
                sub_1407E4890(a1: qword_141ABD470, a2: v102, a3: v101);
              v94 = (_DWORD *)(v104 + 4 * v100);
              v315 = (_DWORD *)(v104 + 4 * v103);
              v93 = v104;
            }
            else
            {
              *v94++ = v98;
            }
            v92 = v97;
          }
          ++v95;
          v91 = *v343;
        }
        while ( v95 < (v343[1] - *v343) >> 3 );
      }
      v319 = v93;
      if ( (dword_141ABD994 & 1) != 0 && dword_141ABD990 <= 1 )
      {
        v105 = &unk_141ABD978;
        while ( 1 )
        {
          v105 = (_QWORD *)v105[2];
          if ( v105 == nullptr || *v105 == 0 )
            break;
          if ( (*((_BYTE *)v105 + 28) & 1) == 0 || *((int *)v105 + 6) > 1 )
            goto LABEL_161;
        }
        v106 = sub_1407E2C90(a1: 2160);
        sub_1407E2EB0(a1: v106, a2: 1099914335, a3: 19968, a4: 1099882446, a5: 0, a6: 1);
        v335 = ((__int64)v94 - v93) >> 2;
        sub_140808920(a1: &v318, a2: &v335);
        sub_1408094C0(a1: &v318, a2: &v316, a3: 0x14193FFB0LL);
        sub_140809550(a1: &v316, a2: &v311, a3: v314);
        sub_1407D6070(a1: v106, a2: &v311);
        sub_140808B00(a1: &v311);
        sub_140808B00(a1: &v316);
        v93 = v319;
        sub_140808B00(a1: &v318);
        if ( (sub_1407E0380(a1: &unk_141ABD978, a2: v106) & 4) != 0 )
          ((void (*)(void))sub_1407CD750)();
      }
LABEL_161:
      sub_1400588B0(a1: v357, a2: &v311, a3: v314);
      v107 = (_QWORD *)v311;
      v108 = (__int64)v94 - v93;
      v109 = v108 >> 2;
      v42 = *(_QWORD *)(v311 + 40);
      v110 = (*(_QWORD *)(v311 + 56) - v42) >> 2;
      if ( v110 >= v108 >> 2 )
        break;
      if ( v108 < 0 )
        goto LABEL_430;
      if ( v42 != 0 )
      {
        v111 = (_QWORD *)(v311 + 40);
        sub_1407E4890(a1: qword_141ABD470, a2: v42, a3: *(_QWORD *)(v311 + 56) - v42);
        v107[7] = 0;
        v107[6] = 0;
        *v111 = 0;
      }
      v112 = v110 + (v110 >> 1);
      if ( v112 <= v109 )
        v112 = v108 >> 2;
      if ( v110 > 0x3FFFFFFFFFFFFFFFLL - (v110 >> 1) )
        v112 = 0x3FFFFFFFFFFFFFFFLL;
      v113 = sub_1407E4490(a1: qword_141ABD470, a2: 4 * v112);
      v107[5] = v113;
      v107[6] = v113;
      v107[7] = v113 + 4 * v112;
      sub_141758A00(a1: v113, a2: v319, a3: v108);
      v107[6] = v113 + 4 * v109;
      v114 = v315;
      if ( (unsigned __int64)v108 >= 0x30D41 )
        goto LABEL_175;
LABEL_185:
      v315 = v114;
      if ( qword_141ABD470 == 0 )
        qword_141ABD470 = sub_1407E4940();
      v311 = 0;
      v312 = nullptr;
      v318 = 0;
      v125 = sub_141750CC0(a1: 32);
      *(_QWORD *)v125 = v125;
      *(_QWORD *)(v125 + 8) = v125;
      *(_QWORD *)(v125 + 16) = v125;
      *(_WORD *)(v125 + 24) = 257;
      *(_QWORD *)&v318 = v125;
      if ( sub_140F6F2A0() != 0 )
      {
        v126 = 0;
        while ( 1 )
        {
          v127 = sub_140F6F2C0(a1: (unsigned int)v126);
          if ( *(int *)(v127 + 8) >= 0 )
          {
            v128 = v127;
            v129 = *(_DWORD *)(v127 + 12);
            v130 = *((_QWORD *)&v311 + 1);
            if ( *((_DWORD **)&v311 + 1) == v312 )
            {
              v131 = *((_QWORD *)&v311 + 1) - v311;
              v132 = (__int64)(*((_QWORD *)&v311 + 1) - v311) >> 2;
              v133 = v132 + 1;
              v134 = v132 + (v132 >> 1);
              if ( v134 <= v132 + 1 )
                v134 = v132 + 1;
              if ( v132 > 0x3FFFFFFFFFFFFFFFLL - (v132 >> 1) )
                v134 = 0x3FFFFFFFFFFFFFFFLL;
              v135 = sub_1407E4490(a1: qword_141ABD470, a2: 4 * v134);
              *(_DWORD *)(v135 + v131) = v129;
              v136 = *((_QWORD *)&v311 + 1);
              sub_141758A00(a1: v135, a2: v311, a3: v130 - v311);
              if ( v136 != v130 )
                sub_141758A00(a1: v135 + v131 + 4, a2: v130, a3: *((_QWORD *)&v311 + 1) - v130);
              if ( (_QWORD)v311 != 0 )
                sub_1407E4890(a1: qword_141ABD470, a2: v311, a3: (char *)v312 - v311);
              *(_QWORD *)&v311 = v135;
              *((_QWORD *)&v311 + 1) = v135 + 4 * v133;
              v312 = (_DWORD *)(v135 + 4 * v134);
            }
            else
            {
              **((_DWORD **)&v311 + 1) = v129;
              *((_QWORD *)&v311 + 1) += 4LL;
            }
            v137 = *(_QWORD *)(v128 + 24);
            if ( (unsigned __int64)(*(_QWORD *)(v128 + 32) - v137) >= 9 )
              break;
          }
LABEL_189:
          if ( ++v126 >= (unsigned __int64)sub_140F6F2A0() )
            goto LABEL_217;
        }
        v138 = 1;
        while ( 1 )
        {
          v139 = *(_QWORD *)(v137 + 8 * v138);
          if ( (unsigned __int8)sub_140CB5650(a1: *(_QWORD *)(qword_141B5AD60 + 72), a2: v128, a3: v139, a4: 0) != 0 )
          {
            v140 = *(_DWORD *)(v139 + 12);
            v141 = v318;
            v142 = *(_QWORD *)(v318 + 8);
            v143 = false;
            if ( *(_BYTE *)(v142 + 25) != 0 )
            {
              v144 = *(_QWORD **)(v318 + 8);
              v145 = (_QWORD *)v318;
              if ( *(_BYTE *)(v318 + 25) != 0 )
                goto LABEL_215;
            }
            else
            {
              v145 = (_QWORD *)v318;
              do
              {
                v144 = (_QWORD *)v142;
                v146 = *(_DWORD *)(v142 + 28);
                v147 = (__int64 *)(v142 + 16);
                if ( v146 >= v140 )
                {
                  v145 = v144;
                  v147 = v144;
                }
                v142 = *v147;
              }
              while ( *(_BYTE *)(v142 + 25) == 0 );
              v143 = v146 >= v140;
              if ( *((_BYTE *)v145 + 25) != 0 )
              {
LABEL_215:
                if ( *((_QWORD *)&v318 + 1) == 0x7FFFFFFFFFFFFFFLL )
LABEL_429:
                  sub_140052D20();
                v148 = sub_141750CC0(a1: 32);
                *(_DWORD *)(v148 + 28) = v140;
                *(_QWORD *)v148 = v141;
                *(_QWORD *)(v148 + 8) = v141;
                *(_QWORD *)(v148 + 16) = v141;
                *(_WORD *)(v148 + 24) = 0;
                v316 = v144;
                v317 = v143;
                sub_140052AA0(a1: &v318, a2: &v316, a3: v148);
                goto LABEL_204;
              }
            }
            if ( v140 < *((_DWORD *)v145 + 7) )
              goto LABEL_215;
          }
LABEL_204:
          ++v138;
          v137 = *(_QWORD *)(v128 + 24);
          if ( v138 >= (*(_QWORD *)(v128 + 32) - v137) >> 3 )
            goto LABEL_189;
        }
      }
LABEL_217:
      sub_1400588B0(a1: v356, a2: &v316, a3: v314);
      v149 = v316;
      v150 = v316 + 5;
      if ( v316 + 5 != (_QWORD *)&v311 )
      {
        v151 = v311;
        v152 = *((_QWORD *)&v311 + 1) - v311;
        v153 = (__int64)(*((_QWORD *)&v311 + 1) - v311) >> 2;
        v42 = v316[5];
        v154 = (v316[7] - v42) >> 2;
        if ( v154 >= v153 )
        {
          v158 = (v316[6] - v42) >> 2;
          v159 = v153 - v158;
          if ( v153 <= v158 )
          {
            v157 = v42 + 4 * v153;
            sub_141758A00(a1: v316[5], a2: v311, a3: *((_QWORD *)&v311 + 1) - v311);
          }
          else
          {
            sub_141758A00(a1: v316[5], a2: v311, a3: v316[6] - v42);
            v160 = v151 + 4 * v158;
            v161 = v149[6];
            sub_141758A00(a1: v161, a2: v160, a3: 4 * v159);
            v157 = v161 + 4 * v159;
          }
        }
        else
        {
          if ( v152 < 0 )
            goto LABEL_430;
          if ( v42 != 0 )
          {
            sub_1407E4890(a1: qword_141ABD470, a2: v42, a3: v316[7] - v42);
            v150[2] = 0;
            v150[1] = 0;
            *v150 = 0;
          }
          v155 = v154 + (v154 >> 1);
          if ( v155 <= v153 )
            v155 = v153;
          if ( v154 > 0x3FFFFFFFFFFFFFFFLL - (v154 >> 1) )
            v155 = 0x3FFFFFFFFFFFFFFFLL;
          v156 = sub_1407E4490(a1: qword_141ABD470, a2: 4 * v155);
          v149[5] = v156;
          v149[6] = v156;
          v149[7] = v156 + 4 * v155;
          sub_141758A00(a1: v156, a2: v151, a3: v152);
          v157 = v156 + 4 * v153;
        }
        v149[6] = v157;
      }
      v162 = sub_140F7AAB0(a1: &qword_141B5FDA8);
      v163 = *(__int64 **)(v162 + 128);
      v164 = *v163;
      if ( v163[1] != *v163 )
      {
        v165 = 0;
        do
        {
          v167 = *(_QWORD *)(v164 + 8 * v165);
          if ( (unsigned __int8)sub_140CB55C0(a1: *(_QWORD *)(qword_141B5AD60 + 72), a2: *(_QWORD *)(v167 + 32)) == 0 )
            goto LABEL_233;
          v168 = *(_DWORD *)(*(_QWORD *)(v167 + 24) + 12LL);
          v169 = v318;
          v170 = *(_QWORD *)(v318 + 8);
          v171 = false;
          if ( *(_BYTE *)(v170 + 25) != 0 )
          {
            v172 = *(_QWORD **)(v318 + 8);
            v173 = (_QWORD *)v318;
            if ( *(_BYTE *)(v318 + 25) == 0 )
              goto LABEL_243;
          }
          else
          {
            v173 = (_QWORD *)v318;
            do
            {
              v172 = (_QWORD *)v170;
              v174 = *(_DWORD *)(v170 + 28);
              v175 = (__int64 *)(v170 + 16);
              if ( v174 >= v168 )
              {
                v173 = v172;
                v175 = v172;
              }
              v170 = *v175;
            }
            while ( *(_BYTE *)(v170 + 25) == 0 );
            v171 = v174 >= v168;
            if ( *((_BYTE *)v173 + 25) == 0 )
            {
LABEL_243:
              if ( v168 >= *((_DWORD *)v173 + 7) )
                goto LABEL_233;
            }
          }
          if ( *((_QWORD *)&v318 + 1) == 0x7FFFFFFFFFFFFFFLL )
            goto LABEL_429;
          v176 = sub_141750CC0(a1: 32);
          *(_DWORD *)(v176 + 28) = v168;
          *(_QWORD *)v176 = v169;
          *(_QWORD *)(v176 + 8) = v169;
          *(_QWORD *)(v176 + 16) = v169;
          *(_WORD *)(v176 + 24) = 0;
          v316 = v172;
          v317 = v171;
          sub_140052AA0(a1: &v318, a2: &v316, a3: v176);
LABEL_233:
          ++v165;
          v166 = *(__int64 **)(v162 + 128);
          v164 = *v166;
        }
        while ( v165 < (v166[1] - *v166) >> 3 );
      }
      v177 = (_DWORD *)v311;
      if ( (_QWORD)v311 != *((_QWORD *)&v311 + 1) )
        *((_QWORD *)&v311 + 1) = v311;
      v178 = (__int64 *)v318;
      v179 = *(__int64 **)v318;
      if ( *(_QWORD *)v318 != (_QWORD)v318 )
      {
        do
        {
          v189 = *((_DWORD *)v179 + 7);
          if ( v177 == v312 )
          {
            v191 = (char *)v177 - v311;
            v192 = (__int64)((__int64)v177 - v311) >> 2;
            v193 = v192 + 1;
            v194 = v192 + (v192 >> 1);
            if ( v194 <= v192 + 1 )
              v194 = v192 + 1;
            if ( v192 > 0x3FFFFFFFFFFFFFFFLL - (v192 >> 1) )
              v194 = 0x3FFFFFFFFFFFFFFFLL;
            v195 = sub_1407E4490(a1: qword_141ABD470, a2: 4 * v194);
            *(_DWORD *)&v191[v195] = v189;
            v196 = *((_DWORD **)&v311 + 1);
            sub_141758A00(a1: v195, a2: v311, a3: (char *)v177 - v311);
            if ( v196 != v177 )
              sub_141758A00(a1: &v191[v195 + 4], a2: v177, a3: *((_QWORD *)&v311 + 1) - (_QWORD)v177);
            if ( (_QWORD)v311 != 0 )
              sub_1407E4890(a1: qword_141ABD470, a2: v311, a3: (char *)v312 - v311);
            *(_QWORD *)&v311 = v195;
            v177 = (_DWORD *)(v195 + 4 * v193);
            *((_QWORD *)&v311 + 1) = v177;
            v312 = (_DWORD *)(v195 + 4 * v194);
            v190 = (__int64 *)v179[2];
            if ( *((_BYTE *)v190 + 25) != 0 )
            {
              do
              {
LABEL_272:
                v197 = (__int64 *)v179[1];
                if ( *((_BYTE *)v197 + 25) != 0 )
                  break;
                v198 = v179;
                v179 = (__int64 *)v179[1];
              }
              while ( v198 == (__int64 *)v197[2] );
              goto LABEL_259;
            }
          }
          else
          {
            *v177 = v189;
            v177 = (_DWORD *)(*((_QWORD *)&v311 + 1) + 4LL);
            *((_QWORD *)&v311 + 1) += 4LL;
            v190 = (__int64 *)v179[2];
            if ( *((_BYTE *)v190 + 25) != 0 )
              goto LABEL_272;
          }
          do
          {
            v197 = v190;
            v190 = (__int64 *)*v190;
          }
          while ( *((_BYTE *)v190 + 25) == 0 );
LABEL_259:
          v179 = v197;
        }
        while ( v197 != v178 );
      }
      sub_1400588B0(a1: v355, a2: &v316, a3: v314);
      v180 = v316;
      v181 = v316 + 5;
      if ( v316 + 5 != (_QWORD *)&v311 )
      {
        v182 = v311;
        v183 = *((_QWORD *)&v311 + 1) - v311;
        v184 = (__int64)(*((_QWORD *)&v311 + 1) - v311) >> 2;
        v42 = v316[5];
        v185 = (v316[7] - v42) >> 2;
        if ( v185 >= v184 )
        {
          v199 = (v316[6] - v42) >> 2;
          v200 = v184 - v199;
          if ( v184 <= v199 )
          {
            v188 = v42 + 4 * v184;
            sub_141758A00(a1: v316[5], a2: v311, a3: *((_QWORD *)&v311 + 1) - v311);
          }
          else
          {
            sub_141758A00(a1: v316[5], a2: v311, a3: v316[6] - v42);
            v201 = v182 + 4 * v199;
            v202 = v180[6];
            sub_141758A00(a1: v202, a2: v201, a3: 4 * v200);
            v188 = v202 + 4 * v200;
          }
        }
        else
        {
          if ( v183 < 0 )
            goto LABEL_430;
          if ( v42 != 0 )
          {
            sub_1407E4890(a1: qword_141ABD470, a2: v42, a3: v316[7] - v42);
            v181[2] = 0;
            v181[1] = 0;
            *v181 = 0;
          }
          v186 = v185 + (v185 >> 1);
          if ( v186 <= v184 )
            v186 = v184;
          if ( v185 > 0x3FFFFFFFFFFFFFFFLL - (v185 >> 1) )
            v186 = 0x3FFFFFFFFFFFFFFFLL;
          v187 = sub_1407E4490(a1: qword_141ABD470, a2: 4 * v186);
          v180[5] = v187;
          v180[6] = v187;
          v180[7] = v187 + 4 * v186;
          sub_141758A00(a1: v187, a2: v182, a3: v183);
          v188 = v187 + 4 * v184;
        }
        v180[6] = v188;
      }
      sub_14004A4D0();
      sub_14004AD20();
      sub_14004DF80();
      if ( qword_141ABD470 != 0 )
      {
        v203 = 0;
        if ( sub_140F7A840() == 0 )
          goto LABEL_296;
      }
      else
      {
        qword_141ABD470 = sub_1407E4940();
        v203 = 0;
        if ( sub_140F7A840() == 0 )
        {
LABEL_296:
          v205 = nullptr;
          v204 = nullptr;
          goto LABEL_297;
        }
      }
      v204 = nullptr;
      v205 = nullptr;
      v206 = 0;
      do
      {
        v207 = sub_140F7A860(a1: (unsigned int)v206);
        if ( *(int *)(v207 + 8) >= 0 )
        {
          v208 = *(_DWORD *)(v207 + 12);
          if ( v205 == v204 )
          {
            v209 = (__int64)v204 - v203;
            v210 = (v209 >> 2) + 1;
            v211 = (unsigned __int64)(v209 >> 2) >> 1;
            v212 = 0x3FFFFFFFFFFFFFFFLL - v211;
            v213 = (v209 >> 2) + v211;
            if ( v213 <= v210 )
              v213 = (v209 >> 2) + 1;
            if ( v209 >> 2 > v212 )
              v213 = 0x3FFFFFFFFFFFFFFFLL;
            v214 = sub_1407E4490(a1: qword_141ABD470, a2: 4 * v213);
            *(_DWORD *)(v214 + v209) = v208;
            sub_141758A00(a1: v214, a2: v203, a3: v209);
            if ( v203 != 0 )
              sub_1407E4890(a1: qword_141ABD470, a2: v203, a3: v209);
            v205 = (_DWORD *)(v214 + 4 * v210);
            v204 = (_DWORD *)(v214 + 4 * v213);
            v203 = v214;
          }
          else
          {
            *v205++ = v208;
          }
        }
        ++v206;
      }
      while ( v206 < sub_140F7A840() );
LABEL_297:
      sub_1400588B0(a1: v354, a2: &v316, a3: v314);
      v215 = v316;
      v216 = (__int64)v205 - v203;
      v217 = v216 >> 2;
      v42 = v316[5];
      v218 = (v316[7] - v42) >> 2;
      if ( v218 >= v216 >> 2 )
      {
        v222 = (v316[6] - v42) >> 2;
        v223 = v217 - v222;
        if ( v217 <= v222 )
        {
          v226 = v42 + 4 * v217;
          sub_141758A00(a1: v316[5], a2: v203, a3: v216);
          v215[6] = v226;
          if ( qword_141ABD470 != 0 )
            goto LABEL_312;
        }
        else
        {
          sub_141758A00(a1: v316[5], a2: v203, a3: v316[6] - v42);
          v224 = v203 + 4 * v222;
          v225 = v215[6];
          sub_141758A00(a1: v225, a2: v224, a3: 4 * v223);
          v215[6] = v225 + 4 * v223;
          if ( qword_141ABD470 != 0 )
            goto LABEL_312;
        }
LABEL_311:
        qword_141ABD470 = sub_1407E4940();
        goto LABEL_312;
      }
      if ( v216 < 0 )
        goto LABEL_430;
      if ( v42 != 0 )
      {
        v219 = v316 + 5;
        sub_1407E4890(a1: qword_141ABD470, a2: v42, a3: v316[7] - v42);
        v215[7] = 0;
        v215[6] = 0;
        *v219 = 0;
      }
      v220 = v218 + (v218 >> 1);
      if ( v220 <= v217 )
        v220 = v216 >> 2;
      if ( v218 > 0x3FFFFFFFFFFFFFFFLL - (v218 >> 1) )
        v220 = 0x3FFFFFFFFFFFFFFFLL;
      v221 = sub_1407E4490(a1: qword_141ABD470, a2: 4 * v220);
      v215[5] = v221;
      v215[6] = v221;
      v215[7] = v221 + 4 * v220;
      sub_141758A00(a1: v221, a2: v203, a3: v216);
      v215[6] = v221 + 4 * v217;
      if ( qword_141ABD470 == 0 )
        goto LABEL_311;
LABEL_312:
      v358 = v204;
      if ( sub_140F4F010() != 0 )
      {
        v310 = 0;
        v227 = nullptr;
        v228 = nullptr;
        v229 = 0;
        do
        {
          v230 = sub_140F7A8D0(a1: (unsigned int)v229);
          if ( *(int *)(v230 + 8) >= 0 )
          {
            v231 = *(_DWORD *)(v230 + 12);
            if ( v228 == v227 )
            {
              v232 = (__int64)v227 - v310;
              v233 = v232 >> 2;
              v234 = (v232 >> 2) + 1;
              v235 = v232;
              v236 = (unsigned __int64)(v232 >> 2) >> 1;
              v237 = 0x3FFFFFFFFFFFFFFFLL - v236;
              v238 = v233 + v236;
              if ( v238 <= v234 )
                v238 = v234;
              if ( v233 > v237 )
                v238 = 0x3FFFFFFFFFFFFFFFLL;
              v239 = sub_1407E4490(a1: qword_141ABD470, a2: 4 * v238);
              *(_DWORD *)(v239 + v235) = v231;
              sub_141758A00(a1: v239, a2: v310, a3: v235);
              if ( v310 != 0 )
                sub_1407E4890(a1: qword_141ABD470, a2: v310, a3: v235);
              v228 = (_DWORD *)(v239 + 4 * v234);
              v227 = (_DWORD *)(v239 + 4 * v238);
              v310 = v239;
            }
            else
            {
              *v228++ = v231;
            }
          }
          ++v229;
        }
        while ( v229 < sub_140F4F010() );
      }
      else
      {
        v310 = 0;
        v228 = nullptr;
        v227 = nullptr;
      }
      v360 = v227;
      sub_1400588B0(a1: v353, a2: &v316, a3: v314);
      v240 = v316;
      v241 = (__int64)v228 - v310;
      v242 = v241 >> 2;
      v42 = v316[5];
      v243 = (v316[7] - v42) >> 2;
      if ( v243 < v241 >> 2 )
      {
        if ( v241 < 0 )
          goto LABEL_430;
        if ( v42 != 0 )
        {
          v244 = v316 + 5;
          sub_1407E4890(a1: qword_141ABD470, a2: v42, a3: v316[7] - v42);
          v240[7] = 0;
          v240[6] = 0;
          *v244 = 0;
        }
        v245 = v243 + (v243 >> 1);
        if ( v245 <= v242 )
          v245 = v241 >> 2;
        if ( v243 > 0x3FFFFFFFFFFFFFFFLL - (v243 >> 1) )
          v245 = 0x3FFFFFFFFFFFFFFFLL;
        v246 = sub_1407E4490(a1: qword_141ABD470, a2: 4 * v245);
        v240[5] = v246;
        v240[6] = v246;
        v240[7] = v246 + 4 * v245;
        sub_141758A00(a1: v246, a2: v310, a3: v241);
        v240[6] = v246 + 4 * v242;
        if ( qword_141ABD470 != 0 )
          goto LABEL_341;
LABEL_340:
        qword_141ABD470 = sub_1407E4940();
        goto LABEL_341;
      }
      v247 = (v316[6] - v42) >> 2;
      v248 = v242 - v247;
      if ( v242 <= v247 )
      {
        v251 = v42 + 4 * v242;
        sub_141758A00(a1: v316[5], a2: v310, a3: v241);
        v240[6] = v251;
        if ( qword_141ABD470 == 0 )
          goto LABEL_340;
      }
      else
      {
        sub_141758A00(a1: v316[5], a2: v310, a3: v316[6] - v42);
        v249 = v310 + 4 * v247;
        v250 = v240[6];
        sub_141758A00(a1: v250, a2: v249, a3: 4 * v248);
        v240[6] = v250 + 4 * v248;
        if ( qword_141ABD470 == 0 )
          goto LABEL_340;
      }
LABEL_341:
      v359 = v203;
      v252 = 0;
      if ( sub_140F459E0() != 0 )
      {
        v253 = nullptr;
        v254 = nullptr;
        v255 = 0;
        do
        {
          v256 = sub_140F45D40(a1: (unsigned int)v255);
          if ( *(int *)(v256 + 8) >= 0 )
          {
            v257 = *(_DWORD *)(v256 + 12);
            if ( v254 == v253 )
            {
              v258 = (__int64)v253 - v252;
              v259 = (v258 >> 2) + 1;
              v260 = (unsigned __int64)(v258 >> 2) >> 1;
              v261 = 0x3FFFFFFFFFFFFFFFLL - v260;
              v262 = (v258 >> 2) + v260;
              if ( v262 <= v259 )
                v262 = (v258 >> 2) + 1;
              if ( v258 >> 2 > v261 )
                v262 = 0x3FFFFFFFFFFFFFFFLL;
              v263 = sub_1407E4490(a1: qword_141ABD470, a2: 4 * v262);
              *(_DWORD *)(v263 + v258) = v257;
              sub_141758A00(a1: v263, a2: v252, a3: v258);
              if ( v252 != 0 )
                sub_1407E4890(a1: qword_141ABD470, a2: v252, a3: v258);
              v254 = (_DWORD *)(v263 + 4 * v259);
              v253 = (_DWORD *)(v263 + 4 * v262);
              v252 = v263;
            }
            else
            {
              *v254++ = v257;
            }
          }
          ++v255;
        }
        while ( v255 < sub_140F459E0() );
      }
      else
      {
        v254 = nullptr;
        v253 = nullptr;
      }
      sub_1400588B0(a1: v352, a2: &v316, a3: v314);
      v264 = v316;
      v265 = (__int64)v254 - v252;
      v266 = v265 >> 2;
      v42 = v316[5];
      v267 = (v316[7] - v42) >> 2;
      if ( v267 >= v265 >> 2 )
      {
        v272 = (v316[6] - v42) >> 2;
        v273 = v266 - v272;
        if ( v266 <= v272 )
        {
          v271 = v42 + 4 * v266;
          sub_141758A00(a1: v316[5], a2: v252, a3: v265);
        }
        else
        {
          sub_141758A00(a1: v316[5], a2: v252, a3: v316[6] - v42);
          v274 = v252 + 4 * v272;
          v275 = v264[6];
          sub_141758A00(a1: v275, a2: v274, a3: 4 * v273);
          v271 = v275 + 4 * v273;
        }
      }
      else
      {
        if ( v265 < 0 )
          goto LABEL_430;
        if ( v42 != 0 )
        {
          v268 = v316 + 5;
          sub_1407E4890(a1: qword_141ABD470, a2: v42, a3: v316[7] - v42);
          v264[7] = 0;
          v264[6] = 0;
          *v268 = 0;
        }
        v269 = v267 + (v267 >> 1);
        if ( v269 <= v266 )
          v269 = v265 >> 2;
        if ( v267 > 0x3FFFFFFFFFFFFFFFLL - (v267 >> 1) )
          v269 = 0x3FFFFFFFFFFFFFFFLL;
        v270 = sub_1407E4490(a1: qword_141ABD470, a2: 4 * v269);
        v264[5] = v270;
        v264[6] = v270;
        v264[7] = v270 + 4 * v269;
        sub_141758A00(a1: v270, a2: v252, a3: v265);
        v271 = v270 + 4 * v266;
      }
      v264[6] = v271;
      v276 = sub_1404D5FF0(a1: &qword_141B5FDA8);
      sub_140FFAD70(a1: v276);
      v277 = sub_140F74740(a1: &qword_141B5FDA8);
      sub_140FFAD70(a1: v277);
      v278 = sub_140002B10(a1: &qword_141B5FDA8);
      sub_140FFAD70(a1: v278);
      v279 = sub_1402EE800(a1: &qword_141B5FDA8);
      sub_140FFAD70(a1: v279);
      sub_14011C380(a1: 0xFFFFFFFFLL);
      v37 = v350;
      if ( v252 != 0 )
        sub_1407E4890(a1: qword_141ABD470, a2: v252, a3: (char *)v253 - v252);
      if ( v310 != 0 )
        sub_1407E4890(a1: qword_141ABD470, a2: v310, a3: (char *)v360 - v310);
      a1 = v351;
      if ( v359 != 0 )
        sub_1407E4890(a1: qword_141ABD470, a2: v359, a3: (char *)v358 - v359);
      sub_140051570(a1: &v318, a2: &v318, a3: *(_QWORD *)(v318 + 8));
      sub_141750D04(a1: v318);
      if ( (_QWORD)v311 != 0 )
        sub_1407E4890(a1: qword_141ABD470, a2: v311, a3: (char *)v312 - v311);
      if ( v319 != 0 )
        sub_1407E4890(a1: qword_141ABD470, a2: v319, a3: (char *)v315 - v319);
      sub_14004E310(a1: v336);
      if ( v375 != 0 )
      {
        sub_1407E4890(a1: qword_141ABD470, a2: v375, a3: v377 - v375);
        v377 = 0;
        v376 = 0;
        v375 = 0;
      }
      if ( v372 != 0 )
      {
        sub_1407E4890(a1: qword_141ABD470, a2: v372, a3: v374 - v372);
        v374 = 0;
        v373 = 0;
        v372 = 0;
      }
      if ( v370 != 0 )
        sub_1407E4890(a1: qword_141ABD470, a2: v370, a3: v371 - v370);
      v46 = v361 + 1;
      v45 = v325;
      if ( v361 + 1 >= (unsigned __int64)((__int64)(*((_QWORD *)&v325 + 1) - v325) >> 3) )
        goto LABEL_383;
    }
    v115 = (*(_QWORD *)(v311 + 48) - v42) >> 2;
    v116 = v109 - v115;
    if ( v109 <= v115 )
    {
      v120 = v42 + 4 * v109;
      sub_141758A00(a1: *(_QWORD *)(v311 + 40), a2: v319, a3: v108);
      v107[6] = v120;
      v114 = v315;
      if ( (unsigned __int64)v108 < 0x30D41 )
        goto LABEL_185;
    }
    else
    {
      v117 = v319;
      sub_141758A00(a1: *(_QWORD *)(v311 + 40), a2: v319, a3: *(_QWORD *)(v311 + 48) - v42);
      v118 = v117 + 4 * v115;
      v119 = v107[6];
      sub_141758A00(a1: v119, a2: v118, a3: 4 * v116);
      v107[6] = v119 + 4 * v116;
      v114 = v315;
      if ( (unsigned __int64)v108 < 0x30D41 )
        goto LABEL_185;
    }
LABEL_175:
    if ( (dword_141ABD994 & 1) != 0 && dword_141ABD990 <= 1 )
    {
      v121 = &unk_141ABD978;
      while ( 1 )
      {
        v121 = (_QWORD *)v121[2];
        if ( v121 == nullptr || *v121 == 0 )
          break;
        if ( (*((_BYTE *)v121 + 28) & 1) == 0 || *((int *)v121 + 6) > 1 )
          goto LABEL_185;
      }
      v122 = sub_1407E2C90(a1: 2160);
      sub_1407E2EB0(a1: v122, a2: 1099914335, a3: 19975, a4: 1099882446, a5: 0, a6: 1);
      v123 = sub_1407E0010(a1: v122, a2: 0x141940B20LL);
      sub_1407D6070(a1: v123, a2: v314);
      v124 = sub_1407E0380(a1: &unk_141ABD978, a2: v122);
      v114 = v315;
      if ( (v124 & 4) != 0 )
      {
        sub_1407CD750(a1: v315);
        v114 = v315;
      }
    }
    goto LABEL_185;
  }
  v32 = v31 >> 3;
  v33 = 1;
  if ( v32 >= 2 )
    v33 = v32;
  v34 = 0;
  while ( 1 )
  {
    v35 = *(_QWORD *)(v30 + 8 * v34);
    if ( *(_BYTE *)(v35 + 73) != 0 )
      break;
    if ( v33 == ++v34 )
      goto LABEL_55;
  }
  v291 = qword_141ABD468;
  v369[0] = 0;
  sub_140809040(a1: v369, a2: 0x14191A400LL, a3: 0xFFFFFFFFLL);
  sub_140824A20(a1: v291, a2: v336, a3: v369);
  sub_140808B00(a1: v369);
  sub_140FE3E30(a1: v369, a2: *(_QWORD *)(v35 + 24));
  sub_14081D7C0(a1: v336, a2: 1, a3: v369, a4: 0);
  v292 = (void (__fastcall ***)(_QWORD, __int64))v369[0];
  if ( v369[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v369[0] + 8LL)) == 0 )
    (**v292)(a1: v292, a2: 1);
  if ( (dword_141ABD994 & 1) != 0 && dword_141ABD990 <= 1 )
  {
    v293 = &unk_141ABD978;
    while ( 1 )
    {
      v293 = (_QWORD *)v293[2];
      if ( v293 == nullptr || *v293 == 0 )
        break;
      if ( (*((_BYTE *)v293 + 28) & 1) == 0 || *((int *)v293 + 6) > 1 )
        goto LABEL_423;
    }
    v294 = sub_1407E2C90(a1: 2160);
    sub_1407E2EB0(a1: v294, a2: 1099914335, a3: 19845, a4: 1099882446, a5: 0, a6: 1);
    sub_14081ED40(a1: v336, a2: v369, a3: 0);
    sub_1407D6070(a1: v294, a2: v369);
    sub_140808B00(a1: v369);
    if ( (sub_1407E0380(a1: &unk_141ABD978, a2: v294) & 4) != 0 )
      ((void (*)(void))sub_1407CD750)();
  }
LABEL_423:
  sub_14081D040(a1: v336);
  sub_14083D320(a1: v362);
LABEL_424:
  LODWORD(v2) = 0;
  v16 = v313;
  if ( v313 != 0 )
    goto LABEL_408;
LABEL_425:
  sub_140808B00(a1: &v334);
  v295 = v324;
  if ( v324 != nullptr && _InterlockedDecrement(v324 + 2) == 0 )
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v295)(a1: v295, a2: 1);
  return (unsigned int)v2;
}
