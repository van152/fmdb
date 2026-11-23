__int64 __fastcall sub_1411C3000(__int64 a1, __int64 a2, __int64 *a3, __int64 a4)
{
  volatile signed __int32 **v4; // rbx
  volatile signed __int32 **v5; // r14
  unsigned int v6; // esi
  __int64 v7; // rdi
  __int64 v8; // rdx
  __int64 v9; // rax
  __int64 v10; // rax
  __int64 *v11; // rcx
  __int64 v12; // rax
  __int64 v13; // rdx
  __int64 v14; // rax
  __int64 v16; // rcx
  __int64 v17; // rax
  char v18; // al
  _DWORD *v19; // rax
  __int64 *v20; // rdi
  __int64 v21; // rax
  __int64 v22; // rcx
  __int64 *v23; // rax
  __int64 v24; // rcx
  __int64 v25; // rcx
  __int64 v26; // rcx
  __int64 v27; // rax
  __int64 v28; // rax
  __int64 v29; // rdx
  __int64 v30; // rcx
  __int64 v31; // rcx
  __int64 v32; // rcx
  __int64 v33; // rax
  __int64 v34; // rcx
  __int64 v35; // rax
  __int64 v36; // rcx
  __int64 v37; // rax
  __int64 v38; // rcx
  __int64 v39; // rax
  __int64 v40; // rcx
  __int64 v41; // rax
  __int64 v42; // rcx
  __int64 v43; // rax
  __int64 v44; // rcx
  __int64 v45; // rax
  __int64 v46; // rax
  __int64 *v47; // rsi
  __int64 v48; // rcx
  __int64 v49; // rdx
  _DWORD *v50; // rcx
  __int64 *v51; // rax
  __int64 *v52; // rcx
  __int64 v53; // rax
  __int64 v54; // rax
  volatile signed __int32 *v55; // rcx
  volatile signed __int32 *v56; // rax
  volatile signed __int32 *v57; // rcx
  __int64 v58; // rax
  __int64 v59; // rax
  __int64 *v60; // rax
  __int64 *v61; // rax
  char v62; // al
  __int64 v63; // rcx
  __int64 v64; // rcx
  _DWORD *v65; // rax
  __int64 *v66; // rdi
  __int64 v67; // rcx
  __int64 *v68; // rax
  __int64 v69; // rcx
  __int64 v70; // rcx
  __int64 *v71; // rax
  __int64 v72; // rax
  __int64 v73; // rcx
  __int64 v74; // rcx
  __int64 v75; // rcx
  __int64 v76; // rcx
  __int64 v77; // rax
  __int64 v78; // rcx
  __int64 v79; // rax
  __int64 v80; // rcx
  __int64 v81; // rax
  __int64 v82; // rcx
  __int64 v83; // rax
  __int64 v84; // rcx
  __int64 v85; // rax
  __int64 v86; // rcx
  __int64 v87; // rax
  __int64 v88; // rcx
  __int64 *v89; // rax
  __int64 v90; // rax
  __int64 v91; // rcx
  __int64 v92; // rax
  int v93; // esi
  __int64 *v94; // rax
  volatile signed __int32 *v95; // rsi
  __int64 v96; // rcx
  __int64 v97; // rax
  volatile signed __int32 *v98; // rcx
  volatile signed __int32 *v99; // rsi
  __int64 v100; // rcx
  volatile signed __int32 *v101; // rcx
  __int64 v102; // rcx
  void (__fastcall ***v103)(_QWORD, __int64); // rcx
  __int64 v104; // rax
  __int64 *v105; // rdx
  __int64 v106; // rcx
  __int64 v107; // rcx
  __int64 v108; // rax
  __int64 v109; // rax
  __int64 v110; // rcx
  __int64 v111; // rax
  __int64 v112; // [rsp+30h] [rbp-50h] BYREF
  int v113; // [rsp+38h] [rbp-48h]
  volatile signed __int32 *v114; // [rsp+40h] [rbp-40h] BYREF
  _QWORD v115[2]; // [rsp+48h] [rbp-38h] BYREF
  volatile signed __int32 *v116; // [rsp+58h] [rbp-28h] BYREF
  volatile signed __int32 *v117; // [rsp+60h] [rbp-20h]
  __int64 *v118; // [rsp+70h] [rbp-10h] BYREF
  _QWORD v119[7]; // [rsp+78h] [rbp-8h] BYREF

  v119[2] = -2;
  v5 = (volatile signed __int32 **)a3;
  v6 = a2;
  v7 = a1;
  if ( (int)a2 <= 1416195699 )
  {
    if ( (int)a2 <= 1315856755 )
    {
      if ( (int)a2 <= 1131307379 )
      {
        if ( (int)a2 <= 1130586720 )
        {
          if ( (int)a2 > 1129082988 )
          {
            if ( (_DWORD)a2 != 1129082989 )
            {
              if ( (_DWORD)a2 == 1129136462 )
              {
                v11 = *(__int64 **)(a1 + 48);
                LOBYTE(v4) = 1;
                if ( v11 != nullptr )
                {
                  v12 = *v11;
                  v13 = 1129136462;
                  goto LABEL_280;
                }
                return (unsigned int)v4;
              }
              if ( (_DWORD)a2 != 1129198950 )
                return sub_140FE3F20(v7, v6, v5);
            }
          }
          else
          {
            if ( (_DWORD)a2 == 1097032556 )
            {
LABEL_198:
              LOBYTE(a2) = -1;
              v54 = sub_1411C2C30(a1, a2);
              sub_1411DE060(v54, &v118);
              sub_14083DB80(&v116, &v118);
              v55 = *v5;
              if ( &v116 != v5 )
              {
                (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)v55 + 16LL))(
                  v55,
                  v5);
                v56 = v116;
                v57 = v117;
                v5[1] = v117;
                *v5 = v56;
                v55 = (volatile signed __int32 *)(sub_14083D4F0(v57) + 8);
                v117 = nullptr;
                v116 = v55;
              }
              (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)v55 + 16LL))(
                v55,
                &v116);
LABEL_275:
              sub_14083B0A0(&v118);
              LOBYTE(v4) = 1;
              return (unsigned int)v4;
            }
            if ( (_DWORD)a2 != 1129072230 && (_DWORD)a2 != 1129082470 )
              return sub_140FE3F20(v7, v6, v5);
          }
          goto LABEL_136;
        }
        if ( (int)a2 > 1130979906 )
        {
          switch ( (_DWORD)a2 )
          {
            case 0x43696243:
              goto LABEL_136;
            case 0x436D6167:
              if ( (unsigned __int8)(*(_BYTE *)(a1 + 44) - 1) <= 0x31u )
              {
                LODWORD(v119[0]) = *(char *)(a1 + 44);
                v118 = (__int64 *)(sub_14083D4F0(a1) + 40);
                sub_14083DFA0(v5, &v118);
                (*(void (__fastcall **)(__int64 *, __int64 **))(*v118 + 16))(v118, &v118);
                goto LABEL_324;
              }
              break;
            case 0x436E6167:
              if ( (unsigned __int8)(*(_BYTE *)(a1 + 45) - 1) <= 0x31u )
              {
                LODWORD(v119[0]) = *(unsigned __int8 *)(a1 + 45);
                v118 = (__int64 *)(sub_14083D4F0(a1) + 40);
                sub_14083DFA0(v5, &v118);
                (*(void (__fastcall **)(__int64 *, __int64 **))(*v118 + 16))(v118, &v118);
                goto LABEL_324;
              }
              break;
            default:
              return sub_140FE3F20(v7, v6, v5);
          }
          goto LABEL_260;
        }
        if ( (_DWORD)a2 != 1130586721 )
        {
          if ( (_DWORD)a2 == 1130589301 )
          {
            if ( *(_BYTE *)(a1 + 47) == 0 )
            {
              v25 = *(_QWORD *)(a1 + 48);
              if ( v25 != 0 )
              {
                a2 = 1130589301;
                goto LABEL_139;
              }
            }
            goto LABEL_260;
          }
          if ( (_DWORD)a2 != 1130591337 )
            return sub_140FE3F20(v7, v6, v5);
          goto LABEL_196;
        }
LABEL_120:
        LODWORD(v4) = 0;
        if ( *(_BYTE *)(a1 + 47) == 0 )
        {
          v24 = *(_QWORD *)(a1 + 48);
          if ( v24 != 0 )
            return sub_140E8A400(v24, (unsigned int)a2, a3);
        }
        return (unsigned int)v4;
      }
      if ( (int)a2 <= 1230197839 )
      {
        if ( (int)a2 > 1131574114 )
        {
          if ( (_DWORD)a2 != 1131574115 && (_DWORD)a2 != 1131635553 && (_DWORD)a2 != 1131639905 )
            return sub_140FE3F20(v7, v6, v5);
        }
        else if ( (_DWORD)a2 != 1131307380 && (_DWORD)a2 != 1131443060 && (_DWORD)a2 != 1131573347 )
        {
          return sub_140FE3F20(v7, v6, v5);
        }
        goto LABEL_120;
      }
      if ( (int)a2 > 1315139176 )
      {
        if ( (_DWORD)a2 != 1315139177 )
        {
          if ( (_DWORD)a2 == 1315333746 )
          {
            v70 = *(_QWORD *)(a1 + 48);
            v71 = (__int64 *)(v70 + 368);
            if ( *(_BYTE *)(v7 + 47) == 0 )
              v71 = (__int64 *)(v70 + 216);
            v72 = *v71;
            if ( v72 != 0
              && (*(_BYTE *)(v70 + 185) != 0 && (v73 = *(_QWORD *)(v72 + 272)) != 0
               || (v73 = *(_QWORD *)(v72 + 264)) != 0) )
            {
              sub_1410668B0(v73, 1315333746, a3);
              LOBYTE(v4) = 1;
              return (unsigned int)v4;
            }
            goto LABEL_260;
          }
          if ( (_DWORD)a2 != 1315725678 )
            return sub_140FE3F20(v7, v6, v5);
        }
      }
      else
      {
        if ( (_DWORD)a2 == 1230197840 )
        {
          if ( *(_BYTE *)(a1 + 41) != 0 )
          {
            LOBYTE(v119[0]) = 1;
            v118 = (__int64 *)(sub_14083D4F0(a1) + 24);
            sub_14083DFA0(v5, &v118);
            (*(void (__fastcall **)(__int64 *, __int64 **))(*v118 + 16))(v118, &v118);
            goto LABEL_324;
          }
          return sub_140FE3F20(v7, v6, v5);
        }
        if ( (_DWORD)a2 == 1232291957 )
        {
          LOBYTE(v119[0]) = *(_BYTE *)(a1 + 46) & 1;
          v118 = (__int64 *)(sub_14083D4F0(a1) + 24);
          sub_14083DFA0(v5, &v118);
          (*(void (__fastcall **)(__int64 *, __int64 **))(*v118 + 16))(v118, &v118);
          goto LABEL_324;
        }
        if ( (_DWORD)a2 != 1315004775 )
          return sub_140FE3F20(v7, v6, v5);
      }
LABEL_152:
      v29 = 368;
      if ( *(_BYTE *)(a1 + 47) == 0 )
        v29 = 216;
      v30 = *(_QWORD *)(*(_QWORD *)(a1 + 48) + v29);
      LOBYTE(v4) = 1;
      if ( v30 != 0 )
      {
        LOBYTE(a4) = 1;
        sub_141042940(v30, v6, a3, a4);
        return (unsigned int)v4;
      }
LABEL_261:
      if ( a3 != &qword_141B5A4A0 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        (*(void (__fastcall **)(__int64, __int64 *, volatile signed __int32 **))(*(_QWORD *)qword_141B5A4A0 + 24LL))(
          qword_141B5A4A0,
          &qword_141B5A4A0,
          v5);
      }
      return (unsigned int)v4;
    }
    if ( (int)a2 > 1415996208 )
    {
      if ( (int)a2 > 1416180083 )
      {
        if ( (int)a2 <= 1416192371 )
        {
          switch ( (_DWORD)a2 )
          {
            case 0x54693174:
              v62 = *(_BYTE *)(a1 + 40);
              LOBYTE(a1) = v62 == 10;
              LOBYTE(v119[0]) = v62 == 10 || v62 == 21;
              v118 = (__int64 *)(sub_14083D4F0(a1) + 24);
              sub_14083DFA0(v5, &v118);
              (*(void (__fastcall **)(__int64 *, __int64 **))(*v118 + 16))(v118, &v118);
              goto LABEL_324;
            case 0x54693274:
              LOBYTE(v119[0]) = *(_BYTE *)(a1 + 40) == 33;
              v118 = (__int64 *)(sub_14083D4F0(a1) + 24);
              sub_14083DFA0(v5, &v118);
              (*(void (__fastcall **)(__int64 *, __int64 **))(*v118 + 16))(v118, &v118);
              goto LABEL_324;
            case 0x54693374:
              v18 = *(_BYTE *)(a1 + 40);
              LOBYTE(a1) = v18 == 9;
              LOBYTE(v119[0]) = v18 == 9 || v18 == 43;
              v118 = (__int64 *)(sub_14083D4F0(a1) + 24);
              sub_14083DFA0(v5, &v118);
              (*(void (__fastcall **)(__int64 *, __int64 **))(*v118 + 16))(v118, &v118);
              goto LABEL_324;
            default:
              break;
          }
          return sub_140FE3F20(v7, v6, v5);
        }
        if ( (_DWORD)a2 == 1416192372 )
        {
          LOBYTE(v119[0]) = *(_BYTE *)(a1 + 40) == 2;
          v118 = (__int64 *)(sub_14083D4F0(a1) + 24);
          sub_14083DFA0(v5, &v118);
          (*(void (__fastcall **)(__int64 *, __int64 **))(*v118 + 16))(v118, &v118);
          goto LABEL_324;
        }
        if ( (_DWORD)a2 != 1416192628 )
        {
          if ( (_DWORD)a2 == 1416193652 )
          {
            LOBYTE(v119[0]) = *(_BYTE *)(a1 + 40) == 0;
            v118 = (__int64 *)(sub_14083D4F0(a1) + 24);
            sub_14083DFA0(v5, &v118);
            (*(void (__fastcall **)(__int64 *, __int64 **))(*v118 + 16))(v118, &v118);
            goto LABEL_324;
          }
          return sub_140FE3F20(v7, v6, v5);
        }
        LOBYTE(v4) = 1;
        LOBYTE(a2) = 1;
        LOBYTE(v119[0]) = (*(__int64 (__fastcall **)(__int64, __int64))(*(_QWORD *)a1 + 352LL))(a1, a2);
        v118 = (__int64 *)(sub_14083D4F0(v74) + 24);
        sub_14083DFA0(v5, &v118);
        (*(void (__fastcall **)(__int64 *, __int64 **))(*v118 + 16))(v118, &v118);
      }
      else
      {
        if ( (int)a2 > 1416061538 )
        {
          switch ( (_DWORD)a2 )
          {
            case 0x54676263:
              LOBYTE(a4) = 2;
              sub_1411C5A90(a1, (unsigned int)&v116, 0, a4, 0);
              v68 = sub_141335F60();
              LODWORD(v119[0]) = (_DWORD)v116;
              v118 = v68;
              sub_14083DFA0(v5, &v118);
              (*(void (__fastcall **)(__int64 *, __int64 **))(*v118 + 16))(v118, &v118);
              goto LABEL_324;
            case 0x54676663:
              LOBYTE(a4) = 2;
              sub_1411C5A30(a1, (unsigned int)v119, 0, a4, 1, 0);
              v118 = sub_141335F60();
              sub_14083DFA0(v5, &v118);
              (*(void (__fastcall **)(__int64 *, __int64 **))(*v118 + 16))(v118, &v118);
              goto LABEL_324;
            case 0x54693074:
              LOBYTE(v119[0]) = *(_BYTE *)(a1 + 40) == 18;
              v118 = (__int64 *)(sub_14083D4F0(a1) + 24);
              sub_14083DFA0(v5, &v118);
              (*(void (__fastcall **)(__int64 *, __int64 **))(*v118 + 16))(v118, &v118);
              goto LABEL_324;
            default:
              break;
          }
          return sub_140FE3F20(v7, v6, v5);
        }
        switch ( (_DWORD)a2 )
        {
          case 0x54666331:
            LOBYTE(v4) = 1;
            LOBYTE(a4) = 1;
            sub_1411C5A30(a1, (unsigned int)v119, 0, a4, 1, 1);
            v118 = sub_141335F60();
            sub_14083DFA0(v5, &v118);
            (*(void (__fastcall **)(__int64 *, __int64 **))(*v118 + 16))(v118, &v118);
            break;
          case 0x54666332:
            LOBYTE(v4) = 1;
            LOBYTE(a3) = 1;
            LOBYTE(a4) = 1;
            sub_1411C5A30(a1, (unsigned int)v119, (_DWORD)a3, a4, 1, 1);
            v118 = sub_141335F60();
            sub_14083DFA0(v5, &v118);
            (*(void (__fastcall **)(__int64 *, __int64 **))(*v118 + 16))(v118, &v118);
            break;
          case 0x54666333:
            LOBYTE(v4) = 1;
            LOBYTE(a3) = 2;
            LOBYTE(a4) = 1;
            sub_1411C5A30(a1, (unsigned int)v119, (_DWORD)a3, a4, 1, 1);
            v118 = sub_141335F60();
            sub_14083DFA0(v5, &v118);
            (*(void (__fastcall **)(__int64 *, __int64 **))(*v118 + 16))(v118, &v118);
            break;
          default:
            return sub_140FE3F20(v7, v6, v5);
        }
      }
      return (unsigned int)v4;
    }
    if ( (int)a2 <= 1415734065 )
    {
      if ( (int)a2 <= 1413703777 )
      {
        if ( (_DWORD)a2 != 1315856756 && (_DWORD)a2 != 1315861330 )
        {
          if ( (_DWORD)a2 == 1347184494 )
          {
            LODWORD(v119[0]) = *(unsigned __int8 *)(*(_QWORD *)(a1 + 48) + 185LL);
            v118 = (__int64 *)(sub_14083D4F0(a1) + 40);
            sub_14083DFA0(v5, &v118);
            (*(void (__fastcall **)(__int64 *, __int64 **))(*v118 + 16))(v118, &v118);
            goto LABEL_324;
          }
          return sub_140FE3F20(v7, v6, v5);
        }
        goto LABEL_152;
      }
      if ( (_DWORD)a2 == 1413703778 )
      {
        v52 = *(__int64 **)(a1 + 48);
        if ( v52 == nullptr )
        {
          LOBYTE(v119[0]) = 0;
          v118 = (__int64 *)(sub_14083D4F0(0) + 24);
          sub_14083DFA0(v5, &v118);
          (*(void (__fastcall **)(__int64 *, __int64 **))(*v118 + 16))(v118, &v118);
          goto LABEL_324;
        }
        v53 = *v52;
        a2 = 1413703778;
        goto LABEL_252;
      }
      if ( (_DWORD)a2 != 1413705326 )
      {
        if ( (_DWORD)a2 != 1415734065 )
          return sub_140FE3F20(v7, v6, v5);
        LOBYTE(v4) = 1;
        LOBYTE(a4) = 1;
        sub_1411C5A90(a1, (unsigned int)&v116, 0, a4, 1);
        v23 = sub_141335F60();
        LODWORD(v119[0]) = (_DWORD)v116;
        v118 = v23;
        sub_14083DFA0(v5, &v118);
        (*(void (__fastcall **)(__int64 *, __int64 **))(*v118 + 16))(v118, &v118);
        return (unsigned int)v4;
      }
LABEL_196:
      v52 = *(__int64 **)(a1 + 48);
      if ( v52 != nullptr )
      {
        v53 = *v52;
        a2 = (unsigned int)a2;
LABEL_252:
        (*(void (__fastcall **)(__int64 *, __int64, __int64 *))(v53 + 16))(v52, a2, a3);
        LOBYTE(v4) = 1;
        return (unsigned int)v4;
      }
      goto LABEL_260;
    }
    if ( (int)a2 > 1415802733 )
    {
      if ( (_DWORD)a2 == 1415802734 )
      {
        v52 = *(__int64 **)(a1 + 48);
        if ( v52 != nullptr )
        {
          v53 = *v52;
          a2 = 1415802734;
          goto LABEL_252;
        }
LABEL_260:
        LOBYTE(v4) = 1;
        goto LABEL_261;
      }
      if ( (_DWORD)a2 == 1415802740 )
        goto LABEL_196;
      if ( (_DWORD)a2 != 1415868001 )
        return sub_140FE3F20(v7, v6, v5);
      if ( *(_BYTE *)(a1 + 47) != 0 )
      {
        v26 = *(_QWORD *)(a1 + 48);
        if ( *(_DWORD *)(v7 + 12) == 145174 )
        {
          LODWORD(v4) = *(unsigned __int8 *)(v26 + 185);
          v27 = sub_1400568B0(qword_141B5FDD0, 145174);
          if ( (_BYTE)v4 == 0 || (v26 = *(_QWORD *)(v27 + 272)) == 0 )
            v26 = *(_QWORD *)(v27 + 264);
        }
        v28 = *(_QWORD *)(v26 + 368);
      }
      else
      {
        v28 = sub_140E65780(*(_QWORD *)(a1 + 48));
      }
      if ( v28 != 0 )
      {
        LODWORD(v119[0]) = *(_DWORD *)(v28 + 8);
        v118 = (__int64 *)(sub_14083D4F0(v26) + 40);
      }
      else
      {
        (*(void (__fastcall **)(__int64, __int64 *, __int64 **))(*(_QWORD *)qword_141B5A4A0 + 24LL))(
          qword_141B5A4A0,
          &qword_141B5A4A0,
          &v118);
      }
      if ( &v118 != (__int64 **)v5 )
      {
        (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)*v5 + 16LL))(*v5, v5);
        (*(void (__fastcall **)(__int64 *, __int64 **, volatile signed __int32 **))(*v118 + 24))(v118, &v118, v5);
      }
    }
    else
    {
      if ( (_DWORD)a2 == 1415734066 )
      {
        LOBYTE(v4) = 1;
        LOBYTE(a3) = 1;
        LOBYTE(a4) = 1;
        sub_1411C5A90(a1, (unsigned int)&v116, (_DWORD)a3, a4, 1);
        v60 = sub_141335F60();
        LODWORD(v119[0]) = (_DWORD)v116;
        v118 = v60;
        sub_14083DFA0(v5, &v118);
        (*(void (__fastcall **)(__int64 *, __int64 **))(*v118 + 16))(v118, &v118);
        return (unsigned int)v4;
      }
      if ( (_DWORD)a2 == 1415734067 )
      {
        LOBYTE(v4) = 1;
        LOBYTE(a3) = 2;
        LOBYTE(a4) = 1;
        sub_1411C5A90(a1, (unsigned int)&v116, (_DWORD)a3, a4, 1);
        v61 = sub_141335F60();
        LODWORD(v119[0]) = (_DWORD)v116;
        v118 = v61;
        sub_14083DFA0(v5, &v118);
        (*(void (__fastcall **)(__int64 *, __int64 **))(*v118 + 16))(v118, &v118);
        return (unsigned int)v4;
      }
      if ( (_DWORD)a2 != 1415736929 )
        return sub_140FE3F20(v7, v6, v5);
      v16 = *(_QWORD *)(a1 + 48);
      if ( *(_BYTE *)(v7 + 47) != 0 )
        v17 = *(_QWORD *)(v16 + 368);
      else
        v17 = sub_140E65780(v16);
      if ( v17 != 0 )
      {
        LODWORD(v119[0]) = *(_DWORD *)(v17 + 8);
        v118 = (__int64 *)(sub_14083D4F0(v16) + 40);
      }
      else
      {
        (*(void (__fastcall **)(__int64, __int64 *, __int64 **))(*(_QWORD *)qword_141B5A4A0 + 24LL))(
          qword_141B5A4A0,
          &qword_141B5A4A0,
          &v118);
      }
      if ( &v118 != (__int64 **)v5 )
      {
        (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)*v5 + 16LL))(*v5, v5);
        (*(void (__fastcall **)(__int64 *, __int64 **, volatile signed __int32 **))(*v118 + 24))(v118, &v118, v5);
      }
    }
    (*(void (__fastcall **)(__int64 *, __int64 **))(*v118 + 16))(v118, &v118);
    goto LABEL_324;
  }
  if ( (int)a2 <= 1665222252 )
  {
    if ( (int)a2 <= 1416520496 )
    {
      if ( (int)a2 <= 1416328000 )
      {
        if ( (int)a2 <= 1416196973 )
        {
          switch ( (_DWORD)a2 )
          {
            case 0x54696E74:
              LOBYTE(v119[0]) = *(_BYTE *)(a1 + 41);
              v118 = (__int64 *)(sub_14083D4F0(a1) + 24);
              sub_14083DFA0(v5, &v118);
              (*(void (__fastcall **)(__int64 *, __int64 **))(*v118 + 16))(v118, &v118);
              goto LABEL_324;
            case 0x54697274:
              LOBYTE(v119[0]) = *(_BYTE *)(a1 + 40) == 1;
              v118 = (__int64 *)(sub_14083D4F0(a1) + 24);
              sub_14083DFA0(v5, &v118);
              (*(void (__fastcall **)(__int64 *, __int64 **))(*v118 + 16))(v118, &v118);
              goto LABEL_324;
            case 0x54697363:
              LOBYTE(v119[0]) = *(_BYTE *)(a1 + 47) == 0;
              v118 = (__int64 *)(sub_14083D4F0(a1) + 24);
              sub_14083DFA0(v5, &v118);
              (*(void (__fastcall **)(__int64 *, __int64 **))(*v118 + 16))(v118, &v118);
              goto LABEL_324;
            default:
              break;
          }
          return sub_140FE3F20(v7, v6, v5);
        }
        if ( (_DWORD)a2 == 1416196974 )
        {
          LOBYTE(v119[0]) = *(_BYTE *)(a1 + 47) == 1;
          v118 = (__int64 *)(sub_14083D4F0(a1) + 24);
          sub_14083DFA0(v5, &v118);
          (*(void (__fastcall **)(__int64 *, __int64 **))(*v118 + 16))(v118, &v118);
          goto LABEL_324;
        }
        if ( (_DWORD)a2 == 1416196980 )
        {
          LOBYTE(v119[0]) = (*(_BYTE *)(a1 + 40) & 0xFD) == 0;
          v118 = (__int64 *)(sub_14083D4F0(a1) + 24);
          sub_14083DFA0(v5, &v118);
          (*(void (__fastcall **)(__int64 *, __int64 **))(*v118 + 16))(v118, &v118);
          goto LABEL_324;
        }
        if ( (_DWORD)a2 != 1416327987 )
          return sub_140FE3F20(v7, v6, v5);
        LOBYTE(a2) = 2;
        LOBYTE(a3) = 1;
        LOBYTE(a4) = 1;
        LODWORD(v119[0]) = (char)sub_1411C5C10(a1, a2, a3, a4);
        v118 = (__int64 *)(sub_14083D4F0(v48) + 40);
        sub_14083DFA0(v5, &v118);
        (*(void (__fastcall **)(__int64 *, __int64 **))(*v118 + 16))(v118, &v118);
        goto LABEL_226;
      }
      if ( (int)a2 > 1416392294 )
      {
        if ( (_DWORD)a2 == 1416392295 )
        {
          LODWORD(v119[0]) = *(char *)(a1 + 42);
          v118 = (__int64 *)(sub_14083D4F0(a1) + 40);
          sub_14083DFA0(v5, &v118);
          (*(void (__fastcall **)(__int64 *, __int64 **))(*v118 + 16))(v118, &v118);
          goto LABEL_324;
        }
        if ( (_DWORD)a2 != 1416520045 )
        {
          if ( (_DWORD)a2 == 1416520052 )
          {
            v49 = 368;
            if ( *(_BYTE *)(a1 + 47) == 0 )
              v49 = 216;
            v50 = *(_DWORD **)(*(_QWORD *)(a1 + 48) + v49);
            if ( v50 != nullptr )
            {
              sub_140FE7190(v50, (int *)&v118);
            }
            else
            {
              LODWORD(v118) = dword_141B60CC0;
              (*(void (__fastcall **)(__int64, __int64 *, _QWORD *))(*(_QWORD *)qword_141B60CC8 + 24LL))(
                qword_141B60CC8,
                &qword_141B60CC8,
                v119);
            }
            sub_140FEAD00((int *)&v118, &v116);
            sub_14083DFA0(v5, &v116);
            (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)v116 + 16LL))(
              v116,
              &v116);
            (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v119[0] + 16LL))(v119[0], v119);
            goto LABEL_324;
          }
          return sub_140FE3F20(v7, v6, v5);
        }
        sub_1407C9510(&v118);
        LODWORD(v117) = 1416851041;
        v116 = (volatile signed __int32 *)(sub_14083D4F0(v75) + 56);
        v4 = &v116;
        sub_14083B5F0(&v118, &v116);
        (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)v116 + 16LL))(
          v116,
          &v116);
        v77 = sub_14083D4F0(v76);
        LODWORD(v117) = 1416851047;
        v116 = (volatile signed __int32 *)(v77 + 56);
        sub_14083B5F0(&v118, &v116);
        (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)v116 + 16LL))(
          v116,
          &v116);
        v79 = sub_14083D4F0(v78);
        LODWORD(v117) = 1416392289;
        v116 = (volatile signed __int32 *)(v79 + 56);
        sub_14083B5F0(&v118, &v116);
        (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)v116 + 16LL))(
          v116,
          &v116);
        v81 = sub_14083D4F0(v80);
        LODWORD(v117) = 1416392295;
        v116 = (volatile signed __int32 *)(v81 + 56);
        sub_14083B5F0(&v118, &v116);
        (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)v116 + 16LL))(
          v116,
          &v116);
        v83 = sub_14083D4F0(v82);
        LODWORD(v117) = 1415802734;
        v116 = (volatile signed __int32 *)(v83 + 56);
        sub_14083B5F0(&v118, &v116);
        (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)v116 + 16LL))(
          v116,
          &v116);
        v85 = sub_14083D4F0(v84);
        LODWORD(v117) = 1416196974;
        v116 = (volatile signed __int32 *)(v85 + 56);
        sub_14083B5F0(&v118, &v116);
        (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)v116 + 16LL))(
          v116,
          &v116);
        v87 = sub_14083D4F0(v86);
        LODWORD(v117) = 1416196963;
        v116 = (volatile signed __int32 *)(v87 + 56);
        sub_14083B5F0(&v118, &v116);
        (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)v116 + 16LL))(
          v116,
          &v116);
        sub_1407C9510(&v116);
        sub_1407EAFE0(v7, (__int64 *)&v116, (__int64 *)&v118);
        sub_14083DDA0(&v114, (__int64 *)&v116);
        sub_14083DFA0(v5, &v114);
        (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)v114 + 16LL))(
          v114,
          &v114);
        sub_140833970(&v116);
        goto LABEL_275;
      }
      switch ( (_DWORD)a2 )
      {
        case 0x546B7341:
          LOBYTE(a2) = 1;
          LOBYTE(a3) = 1;
          LOBYTE(a4) = 1;
          LODWORD(v119[0]) = (char)sub_1411C5C10(a1, a2, a3, a4);
          v118 = (__int64 *)(sub_14083D4F0(v63) + 40);
          sub_14083DFA0(v5, &v118);
          (*(void (__fastcall **)(__int64 *, __int64 **))(*v118 + 16))(v118, &v118);
          break;
        case 0x546B7348:
          LOBYTE(a3) = 1;
          LOBYTE(a4) = 1;
          LODWORD(v119[0]) = (char)sub_1411C5C10(a1, 0, a3, a4);
          v118 = (__int64 *)(sub_14083D4F0(v64) + 40);
          sub_14083DFA0(v5, &v118);
          (*(void (__fastcall **)(__int64 *, __int64 **))(*v118 + 16))(v118, &v118);
          break;
        case 0x546C6E61:
          v19 = *(_DWORD **)(a1 + 24);
          if ( v19 != nullptr && *v19 != 0 )
          {
            v20 = (__int64 *)(a1 + 24);
            v21 = sub_14083D4F0(a1);
            v119[0] = 0;
            if ( v119 != v20 )
            {
              v22 = *v20;
              if ( *v20 != 0 )
                _InterlockedIncrement((volatile signed __int32 *)(v22 - 4));
              v119[0] = v22;
            }
LABEL_98:
            v118 = (__int64 *)(v21 + 136);
            sub_14083DFA0(v5, &v118);
            (*(void (__fastcall **)(__int64 *, __int64 **))(*v118 + 16))(v118, &v118);
            goto LABEL_324;
          }
          sub_140DBEA20(&v114, a1);
          v95 = v114;
          v112 = 0;
          sub_140809040(&v112, 0x141906485LL, 0xFFFFFFFFLL);
          sub_14081AF20(v95, &v116, &v112, 0, 0, 0);
          v97 = sub_14083D4F0(v96);
          v119[0] = 0;
          v98 = v116;
          if ( v116 != nullptr )
            _InterlockedIncrement(v116 - 1);
          goto LABEL_298;
        default:
          return sub_140FE3F20(v7, v6, v5);
      }
LABEL_226:
      LOBYTE(v4) = (*(unsigned __int8 (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)*v5 + 64LL))(
                     *v5,
                     v5) != 0xFF;
      return (unsigned int)v4;
    }
    if ( (int)a2 <= 1416851040 )
    {
      if ( (int)a2 > 1416586032 )
      {
        switch ( (_DWORD)a2 )
        {
          case 0x546F6331:
            LOBYTE(v4) = 1;
            LOBYTE(a4) = 1;
            sub_1411C5AE0(a1, (unsigned int)v119, 0, a4, 1);
            v118 = sub_141335F60();
            sub_14083DFA0(v5, &v118);
            (*(void (__fastcall **)(__int64 *, __int64 **))(*v118 + 16))(v118, &v118);
            break;
          case 0x546F6332:
            LOBYTE(v4) = 1;
            LOBYTE(a3) = 1;
            LOBYTE(a4) = 1;
            sub_1411C5AE0(a1, (unsigned int)v119, (_DWORD)a3, a4, 1);
            v118 = sub_141335F60();
            sub_14083DFA0(v5, &v118);
            (*(void (__fastcall **)(__int64 *, __int64 **))(*v118 + 16))(v118, &v118);
            break;
          case 0x546F6333:
            LOBYTE(v4) = 1;
            LOBYTE(a3) = 2;
            LOBYTE(a4) = 1;
            sub_1411C5AE0(a1, (unsigned int)v119, (_DWORD)a3, a4, 1);
            v118 = sub_141335F60();
            sub_14083DFA0(v5, &v118);
            (*(void (__fastcall **)(__int64 *, __int64 **))(*v118 + 16))(v118, &v118);
            break;
          default:
            return sub_140FE3F20(v7, v6, v5);
        }
      }
      else
      {
        switch ( (_DWORD)a2 )
        {
          case 0x546E6331:
            LOBYTE(v4) = 1;
            LOBYTE(a4) = 1;
            sub_1411C5BC0(a1, (unsigned int)v119, 0, a4, 1);
            v118 = sub_141335F60();
            sub_14083DFA0(v5, &v118);
            (*(void (__fastcall **)(__int64 *, __int64 **))(*v118 + 16))(v118, &v118);
            break;
          case 0x546E6332:
            LOBYTE(v4) = 1;
            LOBYTE(a3) = 1;
            LOBYTE(a4) = 1;
            sub_1411C5BC0(a1, (unsigned int)v119, (_DWORD)a3, a4, 1);
            v118 = sub_141335F60();
            sub_14083DFA0(v5, &v118);
            (*(void (__fastcall **)(__int64 *, __int64 **))(*v118 + 16))(v118, &v118);
            break;
          case 0x546E6333:
            LOBYTE(v4) = 1;
            LOBYTE(a3) = 2;
            LOBYTE(a4) = 1;
            sub_1411C5BC0(a1, (unsigned int)v119, (_DWORD)a3, a4, 1);
            v118 = sub_141335F60();
            sub_14083DFA0(v5, &v118);
            (*(void (__fastcall **)(__int64 *, __int64 **))(*v118 + 16))(v118, &v118);
            break;
          default:
            return sub_140FE3F20(v7, v6, v5);
        }
      }
      return (unsigned int)v4;
    }
    if ( (int)a2 > 1416919407 )
    {
      switch ( (_DWORD)a2 )
      {
        case 0x54747970:
          LODWORD(v119[0]) = *(char *)(a1 + 40);
          v118 = (__int64 *)(sub_14083D4F0(a1) + 40);
          sub_14083DFA0(v5, &v118);
          (*(void (__fastcall **)(__int64 *, __int64 **))(*v118 + 16))(v118, &v118);
          goto LABEL_324;
        case 0x594D414E:
          v88 = *(_QWORD *)(a1 + 48);
          v89 = (__int64 *)(v88 + 368);
          if ( *(_BYTE *)(v7 + 47) == 0 )
            v89 = (__int64 *)(v88 + 216);
          v90 = *v89;
          LOBYTE(v4) = 1;
          if ( v90 != 0
            && (*(_BYTE *)(v88 + 185) != 0 && (v91 = *(_QWORD *)(v90 + 272)) != 0 || (v91 = *(_QWORD *)(v90 + 264)) != 0) )
          {
            LODWORD(v119[0]) = *(char *)(v91 + 1956);
            v118 = (__int64 *)(sub_14083D4F0(v91) + 40);
            sub_14083DFA0(v5, &v118);
            (*(void (__fastcall **)(__int64 *, __int64 **))(*v118 + 16))(v118, &v118);
          }
          return (unsigned int)v4;
        case 0x626B636C:
          LOBYTE(a4) = 3;
          sub_1411C5A90(a1, (unsigned int)&v116, 0, a4, 1);
          v51 = sub_141335F60();
          LODWORD(v119[0]) = (_DWORD)v116;
          v118 = v51;
          sub_14083DFA0(v5, &v118);
          (*(void (__fastcall **)(__int64 *, __int64 **))(*v118 + 16))(v118, &v118);
          goto LABEL_324;
        default:
          break;
      }
      return sub_140FE3F20(v7, v6, v5);
    }
    if ( (_DWORD)a2 != 1416851041 )
    {
      if ( (_DWORD)a2 == 1416851047 )
      {
        LODWORD(v119[0]) = *(char *)(a1 + 43);
        v118 = (__int64 *)(sub_14083D4F0(a1) + 40);
        sub_14083DFA0(v5, &v118);
        (*(void (__fastcall **)(__int64 *, __int64 **))(*v118 + 16))(v118, &v118);
        goto LABEL_324;
      }
      if ( (_DWORD)a2 == 1416914273 )
      {
        LODWORD(v119[0]) = *(_DWORD *)(a1 + 8);
        v118 = (__int64 *)(sub_14083D4F0(a1) + 40);
        sub_14083DFA0(v5, &v118);
        (*(void (__fastcall **)(__int64 *, __int64 **))(*v118 + 16))(v118, &v118);
        goto LABEL_324;
      }
      return sub_140FE3F20(v7, v6, v5);
    }
    v65 = *(_DWORD **)(a1 + 32);
    if ( v65 != nullptr && *v65 != 0 )
    {
      v66 = (__int64 *)(a1 + 32);
      v21 = sub_14083D4F0(a1);
      v119[0] = 0;
      if ( v119 != v66 )
      {
        v67 = *v66;
        if ( *v66 != 0 )
          _InterlockedIncrement((volatile signed __int32 *)(v67 - 4));
        v119[0] = v67;
      }
      goto LABEL_98;
    }
    sub_140DBEA20(&v114, a1);
    v99 = v114;
    v112 = 0;
    sub_140809040(&v112, 0x1418DD4F4LL, 0xFFFFFFFFLL);
    sub_14081AF20(v99, &v116, &v112, 0, 0, 0);
    v97 = sub_14083D4F0(v100);
    v119[0] = 0;
    v98 = v116;
    if ( v116 != nullptr )
      _InterlockedIncrement(v116 - 1);
LABEL_298:
    v119[0] = v98;
    v118 = (__int64 *)(v97 + 136);
    sub_14083DFA0(v5, &v118);
    (*(void (__fastcall **)(__int64 *, __int64 **))(*v118 + 16))(v118, &v118);
    v101 = v116;
    if ( v116 != nullptr && _InterlockedDecrement(v116 - 1) == 0 )
      sub_1412EC9A0((__int64)(v101 - 1));
    v102 = v112;
    if ( v112 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v112 - 4)) == 0 )
      sub_1412EC9A0(v102 - 4);
    v103 = (void (__fastcall ***)(_QWORD, __int64))v114;
    if ( v114 != nullptr && _InterlockedDecrement(v114 + 2) == 0 )
      (**v103)(v103, 1);
    goto LABEL_324;
  }
  if ( (int)a2 > 1683177846 )
  {
    if ( (int)a2 <= 1883333483 )
    {
      if ( (int)a2 > 1818848874 )
      {
        switch ( (_DWORD)a2 )
        {
          case 0x6C696E6B:
            v69 = *(_QWORD *)(a1 + 48);
            if ( v69 != 0 )
              return (*(__int64 (__fastcall **)(__int64, __int64, __int64 *))(*(_QWORD *)v69 + 16LL))(
                       v69,
                       1818848875,
                       a3);
LABEL_292:
            LODWORD(v4) = 0;
            return (unsigned int)v4;
          case 0x6E6D636C:
            LOBYTE(a4) = 3;
            sub_1411C5BC0(a1, (unsigned int)v119, 0, a4, 1);
            v118 = sub_141335F60();
            sub_14083DFA0(v5, &v118);
            (*(void (__fastcall **)(__int64 *, __int64 **))(*v118 + 16))(v118, &v118);
            goto LABEL_324;
          case 0x6F636F6C:
            LOBYTE(a4) = 3;
            sub_1411C5AE0(a1, (unsigned int)v119, 0, a4, 1);
            v118 = sub_141335F60();
            sub_14083DFA0(v5, &v118);
            (*(void (__fastcall **)(__int64 *, __int64 **))(*v118 + 16))(v118, &v118);
            goto LABEL_324;
          default:
            break;
        }
      }
      else
      {
        switch ( (_DWORD)a2 )
        {
          case 0x64534177:
            LOBYTE(v119[0]) = *(_BYTE *)(*(_QWORD *)(a1 + 48) + 185LL);
            v118 = (__int64 *)(sub_14083D4F0(a1) + 24);
            sub_14083DFA0(v5, &v118);
            (*(void (__fastcall **)(__int64 *, __int64 **))(*v118 + 16))(v118, &v118);
            goto LABEL_324;
          case 0x66636F6C:
            LOBYTE(a4) = 3;
            sub_1411C5A30(a1, (unsigned int)v119, 0, a4, 0, 1);
            v118 = sub_141335F60();
            sub_14083DFA0(v5, &v118);
            (*(void (__fastcall **)(__int64 *, __int64 **))(*v118 + 16))(v118, &v118);
            goto LABEL_324;
          case 0x6B746762:
            LOBYTE(a2) = -1;
            v14 = sub_1411C2C30(a1, a2);
            if ( v14 != 0 )
              return (*(__int64 (__fastcall **)(__int64, __int64, volatile signed __int32 **))(*(_QWORD *)v14 + 16LL))(
                       v14,
                       1802790754,
                       v5);
            break;
          default:
            break;
        }
      }
      return sub_140FE3F20(v7, v6, v5);
    }
    if ( (int)a2 > 1952605035 )
    {
      if ( (int)a2 > 1953784438 )
      {
        if ( (_DWORD)a2 == 1953784439 )
        {
          LOBYTE(a2) = -1;
          v92 = sub_1411C2C30(a1, a2);
          sub_1411DE560(v92, &v118);
          v93 = -16777216;
          if ( BYTE2(v118) + BYTE1(v118) + (unsigned int)(unsigned __int8)v118 < 0x180 )
            v93 = -1;
          v94 = sub_141335F60();
          LODWORD(v119[0]) = v93;
          v118 = v94;
          sub_14083DFA0(v5, &v118);
          (*(void (__fastcall **)(__int64 *, __int64 **))(*v118 + 16))(v118, &v118);
          goto LABEL_324;
        }
        if ( (_DWORD)a2 == 1953784684 )
        {
          LOBYTE(a2) = -1;
          v58 = sub_1411C2C30(a1, a2);
          sub_1411DE680(v58, v119);
          v118 = sub_141335F60();
          sub_14083DFA0(v5, &v118);
          (*(void (__fastcall **)(__int64 *, __int64 **))(*v118 + 16))(v118, &v118);
          goto LABEL_324;
        }
      }
      else
      {
        if ( (_DWORD)a2 == 1952605036 )
        {
          LOBYTE(a2) = -1;
          v59 = sub_1411C2C30(a1, a2);
          sub_1411DE560(v59, v119);
          v118 = sub_141335F60();
          sub_14083DFA0(v5, &v118);
          (*(void (__fastcall **)(__int64 *, __int64 **))(*v118 + 16))(v118, &v118);
          goto LABEL_324;
        }
        if ( (_DWORD)a2 == 1952665172 )
        {
          v8 = 368;
          if ( *(_BYTE *)(a1 + 47) == 0 )
            v8 = 216;
          v9 = *(_QWORD *)(*(_QWORD *)(a1 + 48) + v8);
          if ( v9 != 0 )
          {
            v10 = *(_QWORD *)(v9 + 240);
            if ( v10 != 0 )
            {
              LODWORD(v119[0]) = *(_DWORD *)(v10 + 12);
              v118 = (__int64 *)(sub_14083D4F0(216) + 40);
              sub_14083DFA0(v5, &v118);
              (*(void (__fastcall **)(__int64 *, __int64 **))(*v118 + 16))(v118, &v118);
LABEL_324:
              LOBYTE(v4) = 1;
              return (unsigned int)v4;
            }
          }
          goto LABEL_292;
        }
      }
      return sub_140FE3F20(v7, v6, v5);
    }
    if ( (_DWORD)a2 != 1883333484 && (_DWORD)a2 != 1884578668 )
    {
      if ( (_DWORD)a2 == 1937072756 )
      {
        sub_1407C9510(&v118);
        sub_1407C9510(&v116);
        LODWORD(v115[0]) = 1415866742;
        v114 = (volatile signed __int32 *)(sub_14083D4F0(v31) + 56);
        v4 = &v114;
        sub_14083B5F0(&v116, &v114);
        (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)v114 + 16LL))(
          v114,
          &v114);
        v33 = sub_14083D4F0(v32);
        LODWORD(v115[0]) = 1416654707;
        v114 = (volatile signed __int32 *)(v33 + 56);
        sub_14083B5F0(&v116, &v114);
        (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)v114 + 16LL))(
          v114,
          &v114);
        v35 = sub_14083D4F0(v34);
        LODWORD(v115[0]) = 1415870062;
        v114 = (volatile signed __int32 *)(v35 + 56);
        sub_14083B5F0(&v116, &v114);
        (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)v114 + 16LL))(
          v114,
          &v114);
        v37 = sub_14083D4F0(v36);
        LODWORD(v115[0]) = 1415865966;
        v114 = (volatile signed __int32 *)(v37 + 56);
        sub_14083B5F0(&v116, &v114);
        (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)v114 + 16LL))(
          v114,
          &v114);
        v39 = sub_14083D4F0(v38);
        LODWORD(v115[0]) = 1315856756;
        v114 = (volatile signed __int32 *)(v39 + 56);
        sub_14083B5F0(&v116, &v114);
        (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)v114 + 16LL))(
          v114,
          &v114);
        v41 = sub_14083D4F0(v40);
        LODWORD(v115[0]) = 1416196974;
        v114 = (volatile signed __int32 *)(v41 + 56);
        sub_14083B5F0(&v116, &v114);
        (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)v114 + 16LL))(
          v114,
          &v114);
        v43 = sub_14083D4F0(v42);
        LODWORD(v115[0]) = 1413706612;
        v114 = (volatile signed __int32 *)(v43 + 56);
        sub_14083B5F0(&v116, &v114);
        (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)v114 + 16LL))(
          v114,
          &v114);
        v45 = sub_14083D4F0(v44);
        LODWORD(v115[0]) = 1416521062;
        v114 = (volatile signed __int32 *)(v45 + 56);
        sub_14083B5F0(&v116, &v114);
        (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)v114 + 16LL))(
          v114,
          &v114);
        v46 = qword_141B60C30;
        v47 = nullptr;
        if ( qword_141B60C30 != qword_141B60C38 )
        {
          while ( *(_DWORD *)v46 != 1399415892 )
          {
            v46 += 16;
            if ( v46 == qword_141B60C38 )
              goto LABEL_329;
          }
          if ( v46 == qword_141B60C38 )
            v47 = nullptr;
          else
            v47 = *(__int64 **)(v46 + 8);
        }
LABEL_329:
        v104 = sub_14083D4F0(qword_141B60C38);
        v105 = &qword_141B5A4A0;
        if ( v47 != nullptr )
          v105 = v47;
        v115[1] = 0;
        v115[0] = v104 + 8;
        sub_140FEB270(&v114, v105);
        v106 = (unsigned int)v114;
        if ( (unsigned int)v114 <= 0xFEFFFFFF )
        {
          v106 = (unsigned int)v114 & 0x7FFFFF;
          if ( (_DWORD)v106 != 0x7FFFFF && sub_140F5C7E0() == v7 )
          {
            v113 = 1415996228;
            v112 = sub_14083D4F0(v106) + 56;
            sub_14083B5F0(&v116, &v112);
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v112 + 16LL))(v112, &v112);
            v108 = sub_14083D4F0(v107);
            v113 = 1667457857;
            v112 = v108 + 56;
            sub_14083B5F0(&v116, &v112);
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v112 + 16LL))(v112, &v112);
          }
        }
        v109 = sub_14083D4F0(v106);
        v113 = 1665745781;
        v112 = v109 + 56;
        sub_14083B5F0(&v116, &v112);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v112 + 16LL))(v112, &v112);
        v111 = sub_14083D4F0(v110);
        v113 = 1666072914;
        v112 = v111 + 56;
        sub_14083B5F0(&v116, &v112);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v112 + 16LL))(v112, &v112);
        sub_1407EAFE0(v7, (__int64 *)&v118, (__int64 *)&v116);
        sub_14083DDA0(&v112, (__int64 *)&v118);
        sub_14083DFA0(v5, &v112);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v112 + 16LL))(v112, &v112);
        (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v115[0] + 16LL))(v115[0], v115);
        sub_14083B0A0(&v116);
        sub_140833970(&v118);
        LOBYTE(v4) = 1;
        return (unsigned int)v4;
      }
      return sub_140FE3F20(v7, v6, v5);
    }
    goto LABEL_198;
  }
  if ( (int)a2 > 1667460466 )
  {
    if ( (int)a2 > 1668309856 )
    {
      switch ( (_DWORD)a2 )
      {
        case 0x63706361:
          v11 = *(__int64 **)(a1 + 48);
          LOBYTE(v4) = 1;
          if ( v11 == nullptr )
            return (unsigned int)v4;
          v12 = *v11;
          v13 = 1668309857;
          break;
        case 0x63706D73:
          v11 = *(__int64 **)(a1 + 48);
          LOBYTE(v4) = 1;
          if ( v11 == nullptr )
            return (unsigned int)v4;
          v12 = *v11;
          v13 = 1668312435;
          break;
        case 0x63756D63:
          v11 = *(__int64 **)(a1 + 48);
          LOBYTE(v4) = 1;
          if ( v11 != nullptr )
          {
            v12 = *v11;
            v13 = 1668640099;
            break;
          }
          return (unsigned int)v4;
        default:
          return sub_140FE3F20(v7, v6, v5);
      }
LABEL_280:
      (*(void (__fastcall **)(__int64 *, __int64, __int64 *))(v12 + 16))(v11, v13, a3);
      return (unsigned int)v4;
    }
    if ( (_DWORD)a2 == 1667460467 )
    {
      v11 = *(__int64 **)(a1 + 48);
      LOBYTE(v4) = 1;
      if ( v11 != nullptr )
      {
        v12 = *v11;
        v13 = 1667460467;
        goto LABEL_280;
      }
      return (unsigned int)v4;
    }
    if ( (_DWORD)a2 == 1668117603 )
    {
      v11 = *(__int64 **)(a1 + 48);
      LOBYTE(v4) = 1;
      if ( v11 != nullptr )
      {
        v12 = *v11;
        v13 = 1668117603;
        goto LABEL_280;
      }
      return (unsigned int)v4;
    }
    if ( (_DWORD)a2 != 1668117613 )
      return sub_140FE3F20(v7, v6, v5);
    goto LABEL_136;
  }
  if ( (int)a2 > 1667457856 )
  {
    switch ( (_DWORD)a2 )
    {
      case 0x63636341:
        v11 = *(__int64 **)(a1 + 48);
        LOBYTE(v4) = 1;
        if ( v11 != nullptr )
        {
          v12 = *v11;
          v13 = 1667457857;
          goto LABEL_280;
        }
        break;
      case 0x63636361:
        v11 = *(__int64 **)(a1 + 48);
        LOBYTE(v4) = 1;
        if ( v11 != nullptr )
        {
          v12 = *v11;
          v13 = 1667457889;
          goto LABEL_280;
        }
        break;
      case 0x63636D53:
        v11 = *(__int64 **)(a1 + 48);
        LOBYTE(v4) = 1;
        if ( v11 != nullptr )
        {
          v12 = *v11;
          v13 = 1667460435;
          goto LABEL_280;
        }
        break;
      default:
        return sub_140FE3F20(v7, v6, v5);
    }
    return (unsigned int)v4;
  }
  if ( (_DWORD)a2 == 1665222253 || (_DWORD)a2 == 1665941830 )
  {
LABEL_136:
    if ( *(_BYTE *)(a1 + 47) == 0 )
    {
      v25 = *(_QWORD *)(a1 + 48);
      if ( v25 != 0 )
      {
        a2 = (unsigned int)a2;
LABEL_139:
        sub_140E8A400(v25, a2, a3);
        LOBYTE(v4) = 1;
        return (unsigned int)v4;
      }
    }
    goto LABEL_260;
  }
  if ( (_DWORD)a2 != 1667329379 )
    return sub_140FE3F20(v7, v6, v5);
  v11 = *(__int64 **)(a1 + 48);
  LOBYTE(v4) = 1;
  if ( v11 != nullptr )
  {
    v12 = *v11;
    v13 = 1667329379;
    goto LABEL_280;
  }
  return (unsigned int)v4;
}
