__int64 __fastcall sub_1411F4F70(__int64 a1, __int64 a2, __int64 *a3)
{
  __int64 *v3; // rdi
  char v6; // al
  __int64 v7; // r8
  __int64 *v8; // rbx
  __int64 v9; // rax
  __int64 v10; // rcx
  __int64 *v11; // rbx
  __int64 *v12; // r15
  __int64 v13; // rax
  __int64 v14; // rcx
  __int64 v15; // rcx
  __int64 v16; // rax
  __int64 v17; // rax
  __int64 v18; // r8
  __int64 v19; // r8
  __int64 *v20; // rbx
  __int64 *v21; // rdi
  __int64 v22; // rax
  __int64 v23; // rcx
  __int64 v24; // rcx
  __int64 v25; // rax
  __int64 v26; // rax
  __int64 v27; // r8
  __int64 *v28; // rcx
  __int64 v29; // r9
  __int64 v30; // rcx
  __int64 v31; // rax
  __int64 v32; // rax
  __int64 v33; // rax
  __int64 v34; // r8
  unsigned int v35; // eax
  _QWORD *v36; // rcx
  __int64 *v37; // rbx
  __int64 *v38; // r15
  __int64 v39; // rax
  __int64 v40; // rcx
  __int64 v41; // rax
  __int64 *v42; // r13
  __int64 v43; // rax
  __int64 v44; // rcx
  __int64 *v45; // rdx
  char v46; // r14
  __int64 v47; // rcx
  __int64 v48; // rdx
  __int64 *v49; // rax
  __int64 v50; // rax
  __int64 *v51; // r12
  __int64 v52; // rax
  __int64 v53; // rcx
  __int64 *v54; // rdx
  char v55; // r14
  __int64 v56; // rcx
  __int64 v57; // rdx
  __int64 *v58; // rax
  unsigned int v59; // r14d
  __int64 v60; // rax
  __int64 v61; // rcx
  __int64 *v62; // rdx
  unsigned int v63; // eax
  __int64 v64; // rbx
  __int64 *v65; // rax
  __int64 v66; // rax
  __int64 v67; // rax
  __int64 v68; // rcx
  __int64 v69; // rax
  __int64 v70; // rcx
  __int64 v71; // rax
  int v72; // r14d
  __int64 v73; // rax
  __int64 v74; // rcx
  __int64 *v75; // rdx
  unsigned int v76; // eax
  __int64 v77; // rbx
  __int64 *v78; // rax
  __int64 v79; // rax
  __int64 v80; // rax
  __int64 v81; // rcx
  __int64 v82; // rax
  __int64 v83; // rcx
  __int64 v84; // rax
  unsigned int v85; // r12d
  __int64 v86; // rax
  __int64 v87; // rcx
  __int64 *v88; // rdx
  int v89; // r15d
  __int64 v90; // rax
  __int64 v91; // rcx
  __int64 *v92; // rdx
  int v93; // r15d
  __int64 v94; // rcx
  __int64 v95; // rdx
  __int64 *v96; // rax
  char v97; // r13
  __int64 v98; // rcx
  __int64 v99; // rdx
  __int64 *v100; // rax
  char v101; // r13
  __int64 v102; // rbx
  __int64 v103; // rcx
  __int64 v104; // rax
  __int64 v105; // rax
  __int64 v106; // rcx
  int v107; // eax
  int v108; // [rsp+38h] [rbp-18h] BYREF
  __int64 v109; // [rsp+40h] [rbp-10h] BYREF
  __int64 v110; // [rsp+48h] [rbp-8h]
  __int64 v111; // [rsp+50h] [rbp+0h]

  v111 = -2;
  v3 = a3;
  if ( (int)a2 > 1416326960 )
  {
    if ( (int)a2 > 1952605035 )
    {
      switch ( (_DWORD)a2 )
      {
        case 0x7462636C:
          if ( *(_QWORD *)(a1 + 176) != 0 )
          {
            sub_140FE3B40(&v108, a3);
            *(_DWORD *)(*(_QWORD *)(a1 + 176) + 168LL) = v108;
            goto LABEL_35;
          }
          break;
        case 0x74746277:
          if ( *(_QWORD *)(a1 + 176) != 0 )
          {
            sub_140FE3B40(&v108, a3);
            *(_DWORD *)(*(_QWORD *)(a1 + 176) + 164LL) = v108;
            goto LABEL_35;
          }
          break;
        case 0x7474636C:
          if ( *(_QWORD *)(a1 + 176) != 0 )
          {
            sub_140FE3B40(&v108, a3);
            *(_DWORD *)(*(_QWORD *)(a1 + 176) + 160LL) = v108;
            goto LABEL_35;
          }
          break;
        default:
          goto LABEL_25;
      }
      LODWORD(v3) = 0;
      return (unsigned int)v3;
    }
    if ( (unsigned int)(a2 - 1416326961) < 3 )
      return sub_1411D00E0(*(_QWORD *)(a1 + 176), a1, (unsigned int)a2, a3);
  }
  else if ( (int)a2 <= 1413705325 )
  {
    switch ( (_DWORD)a2 )
    {
      case 0x436E6B6E:
        return sub_1411D00E0(*(_QWORD *)(a1 + 176), a1, (unsigned int)a2, a3);
      case 0x504C676E:
        if ( (*(unsigned __int8 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 48LL))(*a3, a3) != 0 )
          v6 = sub_140087030();
        else
          v6 = 0;
        *(_BYTE *)(a1 + 185) = v6;
        goto LABEL_35;
      case 0x54436874:
        return sub_1411D00E0(*(_QWORD *)(a1 + 176), a1, (unsigned int)a2, a3);
      default:
        break;
    }
  }
  else if ( (unsigned int)(a2 - 1416324913) < 3 || (_DWORD)a2 == 1413705326 )
  {
    return sub_1411D00E0(*(_QWORD *)(a1 + 176), a1, (unsigned int)a2, a3);
  }
LABEL_25:
  if ( (_BYTE)word_141B60320 == 0 )
    return sub_140FE2700(a1, (unsigned int)a2, a3);
  if ( (int)a2 <= 1129794662 )
  {
    if ( (int)a2 <= 1128813408 )
    {
      if ( (int)a2 > 1128679267 )
      {
        switch ( (int)a2 )
        {
          case 1128679268:
            LOBYTE(a2) = 24;
            v7 = 1937007732;
            return sub_1411E9540(a1, a2, v7, v3);
          case 1128679269:
          case 1128679270:
          case 1128679271:
          case 1128679272:
          case 1128679273:
          case 1128679274:
          case 1128679275:
          case 1128679276:
          case 1128679281:
          case 1128679282:
            return sub_140FE2700(a1, (unsigned int)a2, a3);
          case 1128679277:
            LOBYTE(a2) = 24;
            v7 = 1668246896;
            return sub_1411E9540(a1, a2, v7, v3);
          case 1128679278:
            LOBYTE(a2) = 24;
            v7 = 1937010285;
            return sub_1411E9540(a1, a2, v7, v3);
          case 1128679279:
            LOBYTE(a2) = 24;
            goto LABEL_254;
          case 1128679280:
            LOBYTE(a2) = 24;
            v7 = 1937008996;
            return sub_1411E9540(a1, a2, v7, v3);
          case 1128679283:
            LOBYTE(a2) = 24;
            v7 = 1718839156;
            return sub_1411E9540(a1, a2, v7, v3);
          default:
            switch ( (int)a2 )
            {
              case 1128746339:
                LOBYTE(a2) = 23;
                v7 = 1668246896;
                return sub_1411E9540(a1, a2, v7, v3);
              case 1128746340:
                LOBYTE(a2) = 23;
                v7 = 1937007732;
                return sub_1411E9540(a1, a2, v7, v3);
              case 1128746341:
              case 1128746342:
              case 1128746344:
              case 1128746345:
              case 1128746346:
              case 1128746347:
              case 1128746348:
              case 1128746349:
                return sub_140FE2700(a1, (unsigned int)a2, a3);
              case 1128746343:
                LOBYTE(a2) = 23;
                v7 = 1735355507;
                return sub_1411E9540(a1, a2, v7, v3);
              case 1128746350:
                LOBYTE(a2) = 23;
                v7 = 1937010285;
                return sub_1411E9540(a1, a2, v7, v3);
              case 1128746351:
                LOBYTE(a2) = 23;
                goto LABEL_254;
              case 1128746352:
                LOBYTE(a2) = 23;
                v7 = 1937008996;
                return sub_1411E9540(a1, a2, v7, v3);
              default:
                switch ( (int)a2 )
                {
                  case 1128808801:
                    LOBYTE(a2) = 7;
                    v7 = 1635021925;
                    return sub_1411E9540(a1, a2, v7, v3);
                  case 1128808803:
                    LOBYTE(a2) = 7;
                    v7 = 1668246896;
                    return sub_1411E9540(a1, a2, v7, v3);
                  case 1128808804:
                    LOBYTE(a2) = 7;
                    v7 = 1937007732;
                    return sub_1411E9540(a1, a2, v7, v3);
                  case 1128808815:
                    LOBYTE(a2) = 7;
                    goto LABEL_254;
                  default:
                    return sub_140FE2700(a1, (unsigned int)a2, a3);
                }
            }
        }
      }
      switch ( (int)a2 )
      {
        case 1128416353:
          LOBYTE(a2) = 9;
          v7 = 1869048947;
          return sub_1411E9540(a1, a2, v7, v3);
        case 1128416354:
        case 1128416357:
        case 1128416359:
        case 1128416360:
        case 1128416361:
        case 1128416362:
        case 1128416363:
        case 1128416364:
        case 1128416365:
        case 1128416366:
          return sub_140FE2700(a1, (unsigned int)a2, a3);
        case 1128416355:
          LOBYTE(a2) = 9;
          v7 = 1668246896;
          return sub_1411E9540(a1, a2, v7, v3);
        case 1128416356:
          LOBYTE(a2) = 9;
          v7 = 1937007732;
          return sub_1411E9540(a1, a2, v7, v3);
        case 1128416358:
          LOBYTE(a2) = 9;
          v7 = 1735355507;
          return sub_1411E9540(a1, a2, v7, v3);
        case 1128416367:
          LOBYTE(a2) = 9;
          goto LABEL_254;
        default:
          switch ( (int)a2 )
          {
            case 1128421217:
              LOBYTE(a2) = 8;
              v7 = 1869048947;
              return sub_1411E9540(a1, a2, v7, v3);
            case 1128421218:
            case 1128421221:
            case 1128421223:
            case 1128421224:
            case 1128421225:
            case 1128421226:
            case 1128421227:
            case 1128421228:
            case 1128421229:
            case 1128421230:
              return sub_140FE2700(a1, (unsigned int)a2, a3);
            case 1128421219:
              LOBYTE(a2) = 8;
              v7 = 1668246896;
              return sub_1411E9540(a1, a2, v7, v3);
            case 1128421220:
              LOBYTE(a2) = 8;
              v7 = 1937007732;
              return sub_1411E9540(a1, a2, v7, v3);
            case 1128421222:
              LOBYTE(a2) = 8;
              v7 = 1735355507;
              return sub_1411E9540(a1, a2, v7, v3);
            case 1128421231:
              LOBYTE(a2) = 8;
              goto LABEL_254;
            default:
              if ( (_DWORD)a2 != 1127379046 )
                return sub_140FE2700(a1, (unsigned int)a2, a3);
              return sub_1411D00E0(*(_QWORD *)(a1 + 176), a1, (unsigned int)a2, a3);
          }
      }
    }
    if ( (int)a2 <= 1129271394 )
    {
      if ( (int)a2 <= 1129070944 )
      {
        switch ( (int)a2 )
        {
          case 1128813409:
            LOBYTE(a2) = 25;
            v7 = 1869048947;
            return sub_1411E9540(a1, a2, v7, v3);
          case 1128813411:
            LOBYTE(a2) = 25;
            v7 = 1668246896;
            return sub_1411E9540(a1, a2, v7, v3);
          case 1128813412:
            LOBYTE(a2) = 25;
            v7 = 1937007732;
            return sub_1411E9540(a1, a2, v7, v3);
          case 1128813414:
            LOBYTE(a2) = 25;
            v7 = 1735355507;
            return sub_1411E9540(a1, a2, v7, v3);
          case 1128813423:
            LOBYTE(a2) = 25;
            goto LABEL_254;
          default:
            return sub_140FE2700(a1, (unsigned int)a2, a3);
        }
      }
      if ( (int)a2 <= 1129075300 )
      {
        switch ( (int)a2 )
        {
          case 1129070945:
            LOBYTE(a2) = 26;
            v7 = 1635021925;
            return sub_1411E9540(a1, a2, v7, v3);
          case 1129070947:
            LOBYTE(a2) = 26;
            v7 = 1668246896;
            return sub_1411E9540(a1, a2, v7, v3);
          case 1129070948:
            LOBYTE(a2) = 26;
            v7 = 1937007732;
            return sub_1411E9540(a1, a2, v7, v3);
          case 1129070959:
            LOBYTE(a2) = 26;
            goto LABEL_254;
          default:
            return sub_140FE2700(a1, (unsigned int)a2, a3);
        }
      }
      switch ( (_DWORD)a2 )
      {
        case 0x434C5265:
          LOBYTE(a2) = 13;
          v7 = 1701733492;
          return sub_1411E9540(a1, a2, v7, v3);
        case 0x434C5267:
          LOBYTE(a2) = 13;
          v7 = 1734438259;
          return sub_1411E9540(a1, a2, v7, v3);
        case 0x434C5273:
          LOBYTE(a2) = 13;
          v7 = 1937007732;
          return sub_1411E9540(a1, a2, v7, v3);
        default:
          break;
      }
    }
    else
    {
      if ( (int)a2 <= 1129272162 )
      {
        switch ( (int)a2 )
        {
          case 1129271395:
            LOBYTE(a2) = 11;
            v7 = 1668246896;
            return sub_1411E9540(a1, a2, v7, v3);
          case 1129271396:
            LOBYTE(a2) = 11;
            v7 = 1937007714;
            return sub_1411E9540(a1, a2, v7, v3);
          case 1129271405:
            LOBYTE(a2) = 11;
            v7 = 1937007732;
            return sub_1411E9540(a1, a2, v7, v3);
          case 1129271406:
            LOBYTE(a2) = 11;
            v7 = 1937010285;
            return sub_1411E9540(a1, a2, v7, v3);
          case 1129271407:
            LOBYTE(a2) = 11;
            goto LABEL_254;
          case 1129271408:
            LOBYTE(a2) = 11;
            v7 = 1937008996;
            return sub_1411E9540(a1, a2, v7, v3);
          default:
            return sub_140FE2700(a1, (unsigned int)a2, a3);
        }
      }
      if ( (int)a2 <= 1129792356 )
      {
        switch ( (int)a2 )
        {
          case 1129272163:
            LOBYTE(a2) = 28;
            v7 = 1668246896;
            return sub_1411E9540(a1, a2, v7, v3);
          case 1129272164:
            LOBYTE(a2) = 28;
            v7 = 1937007714;
            return sub_1411E9540(a1, a2, v7, v3);
          case 1129272173:
            LOBYTE(a2) = 28;
            v7 = 1937007732;
            return sub_1411E9540(a1, a2, v7, v3);
          case 1129272174:
            LOBYTE(a2) = 28;
            v7 = 1937010285;
            return sub_1411E9540(a1, a2, v7, v3);
          case 1129272175:
            LOBYTE(a2) = 28;
            goto LABEL_254;
          case 1129272176:
            LOBYTE(a2) = 28;
            v7 = 1937008996;
            return sub_1411E9540(a1, a2, v7, v3);
          default:
            return sub_140FE2700(a1, (unsigned int)a2, a3);
        }
      }
      if ( (int)a2 > 1129792370 )
      {
        if ( (_DWORD)a2 == 1129792371 )
        {
          LOBYTE(a2) = 18;
          v7 = 1937007732;
          return sub_1411E9540(a1, a2, v7, v3);
        }
        if ( (_DWORD)a2 == 1129794661 )
        {
          LOBYTE(a2) = 14;
          v7 = 1701733492;
          return sub_1411E9540(a1, a2, v7, v3);
        }
      }
      else
      {
        if ( (_DWORD)a2 == 1129792357 )
        {
          LOBYTE(a2) = 18;
          v7 = 1701733492;
          return sub_1411E9540(a1, a2, v7, v3);
        }
        if ( (_DWORD)a2 == 1129792359 )
        {
          LOBYTE(a2) = 18;
          v7 = 1734438259;
          return sub_1411E9540(a1, a2, v7, v3);
        }
      }
    }
    return sub_140FE2700(a1, (unsigned int)a2, a3);
  }
  if ( (int)a2 > 1131245152 )
  {
    if ( (int)a2 <= 1315202668 )
    {
      if ( (int)a2 <= 1312911460 )
      {
        if ( (int)a2 > 1131439729 )
        {
          if ( (int)a2 <= 1312908909 )
          {
            if ( (_DWORD)a2 != 1131439730 && (_DWORD)a2 != 1131570542 )
              return sub_140FE2700(a1, (unsigned int)a2, a3);
            return sub_1411D00E0(*(_QWORD *)(a1 + 176), a1, (unsigned int)a2, a3);
          }
          if ( (_DWORD)a2 != 1312908910 && (_DWORD)a2 != 1312909164 )
            return sub_140FE2700(a1, (unsigned int)a2, a3);
          return sub_1411EAAA0(a1, (unsigned int)a2, a3);
        }
        if ( (_DWORD)a2 == 1131245153 || (_DWORD)a2 == 1131247713 )
          return sub_1411D00E0(*(_QWORD *)(a1 + 176), a1, (unsigned int)a2, a3);
        if ( (_DWORD)a2 != 1131438913 )
          return sub_140FE2700(a1, (unsigned int)a2, a3);
        v110 = 0;
        v109 = sub_14083D4F0(a1) + 8;
        sub_140FEB270(&v108, v3);
        v15 = 0xFFFFFFFFLL;
        if ( (v108 & 0x7FFFFF) != 0x7FFFFF )
          v15 = v108 & 0x7FFFFF;
        v16 = sub_140F629D0(v15);
        if ( v16 != 0 )
        {
          v17 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v16 + 1688LL))(v16);
          if ( v17 != 0 )
          {
            LOBYTE(v18) = 112;
            sub_1411D9840(a1, v17 + *(int *)(*(_QWORD *)(v17 + 8) + 4LL) + 8, v18, 0);
          }
        }
        goto LABEL_400;
      }
      if ( (int)a2 <= 1313302379 )
      {
        if ( (_DWORD)a2 != 1312911461 && (_DWORD)a2 != 1312912238 && (_DWORD)a2 != 1313302126 )
          return sub_140FE2700(a1, (unsigned int)a2, a3);
        return sub_1411EAAA0(a1, (unsigned int)a2, a3);
      }
      if ( (int)a2 <= 1313305453 )
      {
        if ( (_DWORD)a2 != 1313302380 && (_DWORD)a2 != 1313304677 )
          return sub_140FE2700(a1, (unsigned int)a2, a3);
        return sub_1411EAAA0(a1, (unsigned int)a2, a3);
      }
      if ( (_DWORD)a2 == 1313305454 )
        return sub_1411EAAA0(a1, (unsigned int)a2, a3);
      if ( (_DWORD)a2 != 1315006061 )
        return sub_140FE2700(a1, (unsigned int)a2, a3);
      return sub_1411D00E0(*(_QWORD *)(a1 + 176), a1, (unsigned int)a2, a3);
    }
    if ( (int)a2 <= 1415799151 )
    {
      if ( (int)a2 <= 1413705318 )
      {
        if ( (_DWORD)a2 != 1315202669 && (_DWORD)a2 != 1315992166 && (_DWORD)a2 != 1316188262 )
          return sub_140FE2700(a1, (unsigned int)a2, a3);
        return sub_1411D00E0(*(_QWORD *)(a1 + 176), a1, (unsigned int)a2, a3);
      }
      if ( (int)a2 > 1413706351 )
      {
        if ( (_DWORD)a2 == 1413706352 )
        {
          v35 = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
          v36 = *(_QWORD **)(a1 + 24);
          LOBYTE(v3) = 1;
          if ( *(_QWORD **)(a1 + 32) != v36 )
            sub_140FC9D50(*v36, v35, 0);
          return (unsigned int)v3;
        }
        if ( (_DWORD)a2 != 1413706355 )
          return sub_140FE2700(a1, (unsigned int)a2, a3);
        return sub_1411D00E0(*(_QWORD *)(a1 + 176), a1, (unsigned int)a2, a3);
      }
      if ( (_DWORD)a2 != 1413705319 )
      {
        if ( (_DWORD)a2 != 1413706320 )
          return sub_140FE2700(a1, (unsigned int)a2, a3);
        v8 = nullptr;
        v3 = (__int64 *)(*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(*(_QWORD *)*a3 + 176LL))(*a3, a3, 0);
        v9 = *v3;
        v10 = v3[1];
        if ( *v3 != v10 )
        {
          v8 = nullptr;
          while ( *(_DWORD *)v9 != 1347776080 )
          {
            v9 += 16;
            if ( v9 == v10 )
              goto LABEL_268;
          }
          if ( v9 == v10 )
            v8 = nullptr;
          else
            v8 = *(__int64 **)(v9 + 8);
        }
LABEL_268:
        v41 = sub_14083D4F0(v10);
        v42 = &qword_141B5A4A0;
        if ( v8 == nullptr )
          v8 = &qword_141B5A4A0;
        v110 = 0;
        v109 = v41 + 8;
        sub_140FEB270(&v108, v8);
        v43 = *v3;
        v44 = v3[1];
        v45 = nullptr;
        if ( *v3 != v44 )
        {
          while ( *(_DWORD *)v43 != 1347776073 )
          {
            v43 += 16;
            if ( v43 == v44 )
              goto LABEL_304;
          }
          if ( v43 == v44 )
            v45 = nullptr;
          else
            v45 = *(__int64 **)(v43 + 8);
        }
LABEL_304:
        if ( v45 == nullptr )
          v45 = &qword_141B5A4A0;
        v59 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v45 + 80LL))(*v45);
        v60 = *v3;
        v61 = v3[1];
        v62 = nullptr;
        if ( *v3 != v61 )
        {
          while ( *(_DWORD *)v60 != 1347776084 )
          {
            v60 += 16;
            if ( v60 == v61 )
              goto LABEL_352;
          }
          if ( v60 == v61 )
            v62 = nullptr;
          else
            v62 = *(__int64 **)(v60 + 8);
        }
LABEL_352:
        if ( v62 == nullptr )
          v62 = &qword_141B5A4A0;
        v85 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v62 + 64LL))(*v62);
        v86 = *v3;
        v87 = v3[1];
        v88 = nullptr;
        if ( *v3 != v87 )
        {
          while ( *(_DWORD *)v86 != 1347568460 )
          {
            v86 += 16;
            if ( v86 == v87 )
              goto LABEL_370;
          }
          if ( v86 == v87 )
            v88 = nullptr;
          else
            v88 = *(__int64 **)(v86 + 8);
        }
LABEL_370:
        if ( v88 == nullptr )
          v88 = &qword_141B5A4A0;
        v93 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v88 + 80LL))(*v88);
        v94 = *v3;
        v95 = v3[1];
        v96 = nullptr;
        if ( *v3 != v95 )
        {
          while ( *(_DWORD *)v94 != 1347572562 )
          {
            v94 += 16;
            if ( v94 == v95 )
              goto LABEL_388;
          }
          if ( v94 == v95 )
            v96 = nullptr;
          else
            v96 = *(__int64 **)(v94 + 8);
        }
LABEL_388:
        if ( v96 != nullptr )
          v42 = v96;
        v101 = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v42 + 48LL))(*v42, v42);
        if ( (_BYTE)v85 == 0xFF )
          v102 = 0;
        else
          v102 = sub_1411DA480(a1, v85);
        v103 = 0xFFFFFFFFLL;
        if ( (v108 & 0x7FFFFF) != 0x7FFFFF )
          v103 = v108 & 0x7FFFFF;
        v104 = sub_140F629D0(v103);
        if ( v104 != 0 )
        {
          v105 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v104 + 1688LL))(v104);
          if ( v105 != 0 )
          {
            v3 = (__int64 *)v105;
            if ( v102 != 0 )
              sub_1411F6890(a1, v59, v105 + *(_DWORD *)(*(_QWORD *)(v105 + 8) + 4LL) + 8, v102, v101, v93);
            sub_1411D9840(a1, (char *)v3 + *(int *)(v3[1] + 4) + 8, v59, v102);
          }
        }
        goto LABEL_400;
      }
      *(_BYTE *)(a1 + 184) = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
LABEL_35:
      LOBYTE(v3) = 1;
      return (unsigned int)v3;
    }
    if ( (int)a2 > 1417245779 )
    {
      if ( (int)a2 > 1951288645 )
      {
        if ( (_DWORD)a2 == 1951288646 )
        {
          v37 = nullptr;
          v38 = (__int64 *)(*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(*(_QWORD *)*a3 + 176LL))(*a3, a3, 0);
          v39 = *v38;
          v40 = v38[1];
          if ( *v38 != v40 )
          {
            v37 = nullptr;
            while ( *(_DWORD *)v39 != 1347308870 )
            {
              v39 += 16;
              if ( v39 == v40 )
                goto LABEL_295;
            }
            if ( v39 == v40 )
              v37 = nullptr;
            else
              v37 = *(__int64 **)(v39 + 8);
          }
LABEL_295:
          v3 = &qword_141B5A4A0;
          if ( v37 == nullptr )
            v37 = &qword_141B5A4A0;
          v55 = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v37 + 48LL))(*v37, v37);
          v56 = *v38;
          v57 = v38[1];
          v58 = nullptr;
          if ( *v38 != v57 )
          {
            while ( *(_DWORD *)v56 != 1347776084 )
            {
              v56 += 16;
              if ( v56 == v57 )
                goto LABEL_337;
            }
            if ( v56 == v57 )
              v58 = nullptr;
            else
              v58 = *(__int64 **)(v56 + 8);
          }
LABEL_337:
          if ( v58 != nullptr )
            v3 = v58;
          v76 = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v3 + 64LL))(*v3, v3);
          if ( (_BYTE)v76 == 0xFF )
            v77 = 0;
          else
            v77 = sub_1411DA480(a1, v76);
          v78 = *(__int64 **)(a1 + 24);
          LOBYTE(v3) = 1;
          if ( v78 != *(__int64 **)(a1 + 32) )
          {
            v79 = *v78;
            if ( v79 != 0 )
            {
              v80 = *(_QWORD *)(v79 + 128);
              if ( v80 != 0 )
              {
                v81 = v80 + *(int *)(*(_QWORD *)(v80 + 8) + 4LL) + 8;
                v82 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v81 + 1752LL))(v81);
                if ( v77 != 0 && v82 != 0 )
                {
                  v83 = 2080;
                  if ( *(_BYTE *)(a1 + 186) == 0 )
                    v83 = 1344;
                  v84 = sub_1415AA1D0(*(_QWORD *)(v82 + 880) + v83, a1, v77);
                  if ( v84 != 0 )
                    *(_BYTE *)(v84 + 5) = v55;
                }
              }
            }
          }
          return (unsigned int)v3;
        }
        if ( (_DWORD)a2 != 1952936519 )
          return sub_140FE2700(a1, (unsigned int)a2, a3);
        v20 = nullptr;
        v21 = (__int64 *)(*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(*(_QWORD *)*a3 + 176LL))(*a3, a3, 0);
        v22 = *v21;
        v23 = v21[1];
        if ( *v21 != v23 )
        {
          v20 = nullptr;
          while ( *(_DWORD *)v22 != 1347776080 )
          {
            v22 += 16;
            if ( v22 == v23 )
              goto LABEL_286;
          }
          if ( v22 == v23 )
            v20 = nullptr;
          else
            v20 = *(__int64 **)(v22 + 8);
        }
LABEL_286:
        v50 = sub_14083D4F0(v23);
        v51 = &qword_141B5A4A0;
        if ( v20 == nullptr )
          v20 = &qword_141B5A4A0;
        v110 = 0;
        v109 = v50 + 8;
        sub_140FEB270(&v108, v20);
        v52 = *v21;
        v53 = v21[1];
        v54 = nullptr;
        if ( *v21 != v53 )
        {
          while ( *(_DWORD *)v52 != 1346851433 )
          {
            v52 += 16;
            if ( v52 == v53 )
              goto LABEL_328;
          }
          if ( v52 == v53 )
            v54 = nullptr;
          else
            v54 = *(__int64 **)(v52 + 8);
        }
LABEL_328:
        if ( v54 == nullptr )
          v54 = &qword_141B5A4A0;
        v72 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v54 + 64LL))(*v54);
        v73 = *v21;
        v74 = v21[1];
        v75 = nullptr;
        if ( *v21 != v74 )
        {
          while ( *(_DWORD *)v73 != 1346851425 )
          {
            v73 += 16;
            if ( v73 == v74 )
              goto LABEL_361;
          }
          if ( v73 == v74 )
            v75 = nullptr;
          else
            v75 = *(__int64 **)(v73 + 8);
        }
LABEL_361:
        if ( v75 == nullptr )
          v75 = &qword_141B5A4A0;
        v89 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v75 + 64LL))(*v75);
        v90 = *v21;
        v91 = v21[1];
        v92 = nullptr;
        if ( *v21 != v91 )
        {
          while ( *(_DWORD *)v90 != 1347776084 )
          {
            v90 += 16;
            if ( v90 == v91 )
              goto LABEL_379;
          }
          if ( v90 == v91 )
            v92 = nullptr;
          else
            v92 = *(__int64 **)(v90 + 8);
        }
LABEL_379:
        if ( v92 == nullptr )
          v92 = &qword_141B5A4A0;
        v97 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v92 + 64LL))(*v92);
        v98 = *v21;
        v99 = v21[1];
        v100 = nullptr;
        if ( *v21 != v99 )
        {
          while ( *(_DWORD *)v98 != 1347568460 )
          {
            v98 += 16;
            if ( v98 == v99 )
              goto LABEL_402;
          }
          if ( v98 == v99 )
            v100 = nullptr;
          else
            v100 = *(__int64 **)(v98 + 8);
        }
LABEL_402:
        if ( v100 != nullptr )
          v51 = v100;
        LODWORD(v3) = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v51 + 80LL))(*v51, v51);
        v106 = 0xFFFFFFFFLL;
        if ( (v108 & 0x7FFFFF) != 0x7FFFFF )
          v106 = v108 & 0x7FFFFF;
        v107 = sub_140F629D0(v106);
        sub_1411DCB30(a1, v107, v72, v89, v97, (_DWORD)v3);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v109 + 16LL))(v109, &v109);
        goto LABEL_35;
      }
      if ( (_DWORD)a2 != 1417245780 )
      {
        if ( (_DWORD)a2 != 1950443091 )
          return sub_140FE2700(a1, (unsigned int)a2, a3);
        v11 = nullptr;
        v12 = (__int64 *)(*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(*(_QWORD *)*a3 + 176LL))(*a3, a3, 0);
        v13 = *v12;
        v14 = v12[1];
        if ( *v12 != v14 )
        {
          v11 = nullptr;
          while ( *(_DWORD *)v13 != 1346463315 )
          {
            v13 += 16;
            if ( v13 == v14 )
              goto LABEL_277;
          }
          if ( v13 == v14 )
            v11 = nullptr;
          else
            v11 = *(__int64 **)(v13 + 8);
        }
LABEL_277:
        v3 = &qword_141B5A4A0;
        if ( v11 == nullptr )
          v11 = &qword_141B5A4A0;
        v46 = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v11 + 64LL))(*v11, v11);
        v47 = *v12;
        v48 = v12[1];
        v49 = nullptr;
        if ( *v12 != v48 )
        {
          while ( *(_DWORD *)v47 != 1347776084 )
          {
            v47 += 16;
            if ( v47 == v48 )
              goto LABEL_313;
          }
          if ( v47 == v48 )
            v49 = nullptr;
          else
            v49 = *(__int64 **)(v47 + 8);
        }
LABEL_313:
        if ( v49 != nullptr )
          v3 = v49;
        v63 = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v3 + 64LL))(*v3, v3);
        if ( (_BYTE)v63 == 0xFF )
          v64 = 0;
        else
          v64 = sub_1411DA480(a1, v63);
        v65 = *(__int64 **)(a1 + 24);
        LOBYTE(v3) = 1;
        if ( v65 != *(__int64 **)(a1 + 32) )
        {
          v66 = *v65;
          if ( v66 != 0 )
          {
            v67 = *(_QWORD *)(v66 + 128);
            if ( v67 != 0 )
            {
              v68 = v67 + *(int *)(*(_QWORD *)(v67 + 8) + 4LL) + 8;
              v69 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v68 + 1752LL))(v68);
              if ( v64 != 0 && v69 != 0 )
              {
                v70 = 2080;
                if ( *(_BYTE *)(a1 + 186) == 0 )
                  v70 = 1344;
                v71 = sub_1415AA1D0(*(_QWORD *)(v69 + 880) + v70, a1, v64);
                if ( v71 != 0 )
                  *(_BYTE *)(v71 + 4) = v46;
              }
            }
          }
        }
        return (unsigned int)v3;
      }
      v110 = 0;
      v109 = sub_14083D4F0(a1) + 8;
      sub_140FEB270(&v108, v3);
      v30 = 0xFFFFFFFFLL;
      if ( (v108 & 0x7FFFFF) != 0x7FFFFF )
        v30 = v108 & 0x7FFFFF;
      v31 = sub_140F629D0(v30);
      if ( v31 != 0 )
      {
        v32 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v31 + 1688LL))(v31);
        if ( v32 != 0 )
        {
          v3 = (__int64 *)v32;
          v33 = sub_1411EA560(a1, 0);
          LOBYTE(v34) = -106;
          sub_1411D9840(a1, (char *)v3 + *(int *)(v3[1] + 4) + 8, v34, v33);
        }
      }
LABEL_400:
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v109 + 16LL))(v109, &v109);
      goto LABEL_35;
    }
    switch ( (_DWORD)a2 )
    {
      case 0x54636170:
        v19 = 1415799152;
        break;
      case 0x54667454:
        v110 = 0;
        v109 = sub_14083D4F0(a1) + 8;
        sub_140FEB270(&v108, v3);
        v24 = 0xFFFFFFFFLL;
        if ( (v108 & 0x7FFFFF) != 0x7FFFFF )
          v24 = v108 & 0x7FFFFF;
        v25 = sub_140F629D0(v24);
        if ( v25 != 0 )
        {
          v26 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v25 + 1688LL))(v25);
          if ( v26 != 0 )
          {
            v28 = *(__int64 **)(a1 + 24);
            if ( v28 == *(__int64 **)(a1 + 32) )
              v29 = 0;
            else
              v29 = *v28;
            LOBYTE(v27) = -106;
            sub_1411D9840(a1, v26 + *(int *)(*(_QWORD *)(v26 + 8) + 4LL) + 8, v27, v29);
          }
        }
        goto LABEL_400;
      case 0x54766370:
        v19 = 1417044848;
        break;
      default:
        return sub_140FE2700(a1, (unsigned int)a2, a3);
    }
    return sub_1411F76F0(a1, 0, v19, v3);
  }
  if ( (int)a2 > 1129926754 )
  {
    if ( (int)a2 <= 1129927522 )
    {
      switch ( (int)a2 )
      {
        case 1129926755:
          LOBYTE(a2) = 10;
          v7 = 1668246896;
          return sub_1411E9540(a1, a2, v7, v3);
        case 1129926756:
          LOBYTE(a2) = 10;
          v7 = 1937007714;
          return sub_1411E9540(a1, a2, v7, v3);
        case 1129926765:
          LOBYTE(a2) = 10;
          v7 = 1937007732;
          return sub_1411E9540(a1, a2, v7, v3);
        case 1129926766:
          LOBYTE(a2) = 10;
          v7 = 1937010285;
          return sub_1411E9540(a1, a2, v7, v3);
        case 1129926767:
          LOBYTE(a2) = 10;
LABEL_254:
          v7 = 1869899892;
          return sub_1411E9540(a1, a2, v7, v3);
        case 1129926768:
          LOBYTE(a2) = 10;
          v7 = 1937008996;
          return sub_1411E9540(a1, a2, v7, v3);
        default:
          return sub_140FE2700(a1, (unsigned int)a2, a3);
      }
    }
    if ( (int)a2 <= 1130456686 )
    {
      switch ( (int)a2 )
      {
        case 1129927523:
          LOBYTE(a2) = 27;
          v7 = 1668246896;
          return sub_1411E9540(a1, a2, v7, v3);
        case 1129927524:
          LOBYTE(a2) = 27;
          v7 = 1937007714;
          return sub_1411E9540(a1, a2, v7, v3);
        case 1129927533:
          LOBYTE(a2) = 27;
          v7 = 1937007732;
          return sub_1411E9540(a1, a2, v7, v3);
        case 1129927534:
          LOBYTE(a2) = 27;
          v7 = 1937010285;
          return sub_1411E9540(a1, a2, v7, v3);
        case 1129927535:
          LOBYTE(a2) = 27;
          goto LABEL_254;
        case 1129927536:
          LOBYTE(a2) = 27;
          v7 = 1937008996;
          return sub_1411E9540(a1, a2, v7, v3);
        default:
          return sub_140FE2700(a1, (unsigned int)a2, a3);
      }
    }
    if ( (int)a2 > 1130460259 )
    {
      if ( (_DWORD)a2 != 1130460260 && (_DWORD)a2 != 1130653295 )
        return sub_140FE2700(a1, (unsigned int)a2, a3);
    }
    else if ( (_DWORD)a2 != 1130456687 && (_DWORD)a2 != 1130458228 )
    {
      return sub_140FE2700(a1, (unsigned int)a2, a3);
    }
    return sub_1411D00E0(*(_QWORD *)(a1 + 176), a1, (unsigned int)a2, a3);
  }
  if ( (int)a2 <= 1129796452 )
  {
    if ( (int)a2 <= 1129796196 )
    {
      if ( (_DWORD)a2 == 1129794663 )
      {
        LOBYTE(a2) = 14;
        v7 = 1734438259;
        return sub_1411E9540(a1, a2, v7, v3);
      }
      if ( (_DWORD)a2 == 1129794675 )
      {
        LOBYTE(a2) = 14;
        v7 = 1937007732;
        return sub_1411E9540(a1, a2, v7, v3);
      }
      return sub_140FE2700(a1, (unsigned int)a2, a3);
    }
    if ( (_DWORD)a2 == 1129796197 )
    {
      LOBYTE(a2) = 12;
      v7 = 1701733492;
      return sub_1411E9540(a1, a2, v7, v3);
    }
    if ( (_DWORD)a2 == 1129796199 )
    {
      LOBYTE(a2) = 12;
      v7 = 1734438259;
      return sub_1411E9540(a1, a2, v7, v3);
    }
    if ( (_DWORD)a2 != 1129796211 )
      return sub_140FE2700(a1, (unsigned int)a2, a3);
    LOBYTE(a2) = 12;
    v7 = 1937007732;
  }
  else
  {
    if ( (int)a2 > 1129797476 )
    {
      switch ( (_DWORD)a2 )
      {
        case 0x43575765:
          LOBYTE(a2) = 15;
          v7 = 1701733492;
          return sub_1411E9540(a1, a2, v7, v3);
        case 0x43575767:
          LOBYTE(a2) = 15;
          v7 = 1734438259;
          return sub_1411E9540(a1, a2, v7, v3);
        case 0x43575773:
          LOBYTE(a2) = 15;
          v7 = 1937007732;
          return sub_1411E9540(a1, a2, v7, v3);
        default:
          break;
      }
      return sub_140FE2700(a1, (unsigned int)a2, a3);
    }
    if ( (_DWORD)a2 == 1129796453 )
    {
      LOBYTE(a2) = 19;
      v7 = 1701733492;
      return sub_1411E9540(a1, a2, v7, v3);
    }
    if ( (_DWORD)a2 == 1129796455 )
    {
      LOBYTE(a2) = 19;
      v7 = 1734438259;
      return sub_1411E9540(a1, a2, v7, v3);
    }
    if ( (_DWORD)a2 != 1129796467 )
      return sub_140FE2700(a1, (unsigned int)a2, a3);
    LOBYTE(a2) = 19;
    v7 = 1937007732;
  }
  return sub_1411E9540(a1, a2, v7, v3);
}
