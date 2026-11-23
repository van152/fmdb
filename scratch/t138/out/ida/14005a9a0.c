__int64 __fastcall sub_14005A9A0(__int64 a1, __int64 a2, __int64 a3, __int64 a4)
{
  unsigned int v4; // ebp
  __int64 v5; // rbx
  unsigned int v6; // esi
  __int64 v7; // rdi
  unsigned __int64 v8; // rax
  __int64 v9; // rcx
  int v11; // ecx
  int v12; // ecx
  int v13; // ecx
  int v14; // ecx
  int v15; // ecx
  int v16; // ecx
  __int64 v17; // rdx
  __int64 v18; // rdx
  __int64 v19; // rdx
  __int64 v20; // rsi
  __int64 v21; // rsi
  __int64 v22; // rsi
  __int64 v23; // rax
  unsigned int v24; // eax
  __int64 v25; // rax
  __int64 v26; // rax
  __int64 v27; // rax
  __int64 v28; // rsi
  __int64 v29; // rax
  __int64 v30; // rax
  __int64 v31; // rax
  char v32; // al
  __int64 v33; // rcx
  void (__fastcall ***v34)(_QWORD, __int64); // rcx
  void (__fastcall **v35)(_QWORD, __int64); // rax
  unsigned int v36; // ebx
  _QWORD *v37; // rbp
  __int64 v38; // r14
  __int64 v39; // rsi
  __int64 v40; // rax
  __int64 v41; // r15
  __int64 v42; // rax
  __int64 v43; // rax
  char v44; // bl
  __int64 v45; // r8
  __int64 v46; // rsi
  __int64 v47; // rdi
  __int64 v48; // r8
  _BYTE v49[8]; // [rsp+30h] [rbp-98h] BYREF
  _BYTE v50[16]; // [rsp+38h] [rbp-90h] BYREF
  __int64 v51; // [rsp+48h] [rbp-80h] BYREF
  _QWORD v52[7]; // [rsp+50h] [rbp-78h] BYREF
  __int64 v53; // [rsp+88h] [rbp-40h] BYREF
  _QWORD v54[7]; // [rsp+90h] [rbp-38h] BYREF

  v5 = a3;
  v6 = a2;
  v7 = a1;
  LOBYTE(v4) = 1;
  if ( (int)a2 <= 1835823170 )
  {
    if ( (int)a2 > 1667658340 )
    {
      if ( (int)a2 > 1735943778 )
      {
        if ( (int)a2 <= 1818518373 )
        {
          if ( (int)a2 > 1818517867 )
          {
            if ( (_DWORD)a2 == 1818517868 || (_DWORD)a2 == 1818517875 || (_DWORD)a2 == 1818518371 )
              return v4;
          }
          else
          {
            switch ( (_DWORD)a2 )
            {
              case 0x67786663:
                return v4;
              case 0x696E6974:
                v36 = sub_140124190(a1, a2: 1768843636, a3);
                sub_14005A740(a1: v7);
                return v36;
              case 0x6C646163:
                return sub_14005C0B0(a1);
              default:
                break;
            }
          }
          return (unsigned int)sub_140124190(a1: v7, a2: v6, a3: v5);
        }
        if ( (int)a2 > 1818519154 )
        {
          if ( (int)a2 > 1818522994 )
          {
            if ( (_DWORD)a2 == 1818522995 )
            {
              sub_14005C1E0(a1);
              return v4;
            }
            if ( (_DWORD)a2 == 1818719329 )
            {
              v22 = qword_141ABD830;
              v23 = sub_140835850(a1: a3, a2: 1768169504);
              v24 = sub_14083E0C0(a1: v23);
              sub_140097B40(a1: v22, a2: v24);
              return v4;
            }
          }
          else
          {
            if ( (_DWORD)a2 == 1818519155 )
              return v4;
            if ( (_DWORD)a2 == 1818522739 )
            {
              sub_1400635E0(a1);
              return v4;
            }
          }
          return (unsigned int)sub_140124190(a1: v7, a2: v6, a3: v5);
        }
        if ( (_DWORD)a2 != 1818518374 )
        {
          if ( (_DWORD)a2 == 1818518627 )
            return sub_14005C310(a1, a2: a3);
          if ( (_DWORD)a2 == 1818519139 )
            return v4;
          return (unsigned int)sub_140124190(a1: v7, a2: v6, a3: v5);
        }
        v38 = qword_141ABD830;
        if ( (unsigned __int8)sub_1408357E0(a1: a3, a2: 1936093036) != 0 )
        {
          v39 = sub_140835850(a1: v5, a2: 1936093036);
          v40 = sub_140843600();
          sub_1408436F0(a1: v40, a2: v52, a3: v39);
        }
        else
        {
          sub_1407D5DC0(a1: qword_141ABD878, a2: v52, a3: &qword_141B59838);
        }
        v41 = v52[0];
        v42 = sub_140835850(a1: v5, a2: 1936091500);
        sub_14083E100(a1: v42, a2: v50);
        sub_1407D5F40(a1: v52, a2: v50);
        sub_140808B00(a1: v50);
        v43 = sub_140835850(a1: v5, a2: 1937013104);
        sub_14083E100(a1: v43, a2: v49);
        sub_1407D8AC0(a1: v50, a2: v49);
        sub_140808B00(a1: v49);
        v44 = sub_140F6F400();
        v54[0] = v41;
        if ( v41 != 0 )
          _InterlockedIncrement((volatile signed __int32 *)(v41 + 8));
        if ( (unsigned __int8)sub_1400959F0(a1: v38, a2: v54, a3: v52, a4: v50) != 0 )
        {
          if ( v44 == 0 )
          {
            sub_1400329B0(a1: qword_141ABF5C0);
            sub_14000FDF0(a1: (_QWORD *)qword_141ABF5C0);
          }
          sub_140014610(a1: qword_141ABF5C0, a2: 0);
          LOBYTE(v45) = -1;
          sub_140016B80(a1: qword_141ABF5C0, a2: 0, a3: v45);
          sub_140147750(a1: v7, a2: 1919705960, a3: 0);
          if ( *(_QWORD *)(v38 + 320) != *(_QWORD *)(v38 + 328) )
            sub_14009F680(a1: v38, a2: &qword_141B59EE0);
        }
        else
        {
          v46 = qword_141B5AD60;
          v47 = sub_1400015F0(a1: v52);
          v51 = 0;
          sub_140809040(a1: &v51, a2: 0x141941E03LL, a3: 0xFFFFFFFFLL);
          sub_140809550(a1: &v51, a2: v49, a3: v47);
          LOBYTE(v48) = 1;
          (*(void (__fastcall **)(__int64, _BYTE *, __int64, _QWORD))(*(_QWORD *)v46 + 120LL))(
            a1: v46,
            a2: v49,
            a3: v48,
            a4: 0);
          sub_140808B00(a1: v49);
          sub_140808B00(a1: &v51);
        }
        sub_140808B00(a1: v52);
        if ( v41 == 0 || _InterlockedDecrement((volatile signed __int32 *)(v41 + 8)) != 0 )
          return v4;
        v35 = *(void (__fastcall ***)(_QWORD, __int64))v41;
        v34 = (void (__fastcall ***)(_QWORD, __int64))v41;
LABEL_235:
        (*v35)(a1: v34, a2: 1);
        return v4;
      }
      if ( (int)a2 > 1668112747 )
      {
        if ( (int)a2 <= 1684825204 )
        {
          switch ( (_DWORD)a2 )
          {
            case 0x636D616C:
              return sub_14005BA40();
            case 0x636E6463:
              return sub_14005A4C0(a1, a2: a3);
            case 0x63726D72:
              sub_14005F0A0(a1);
              return v4;
            default:
              break;
          }
        }
        else if ( (int)a2 > 1718776435 )
        {
          if ( (_DWORD)a2 == 1718776436 )
          {
            if ( *(_BYTE *)(qword_141ABD830 + 1347) != 0 )
              *(_BYTE *)(qword_141ABD830 + 1347) = 0;
            else
              *(_BYTE *)(qword_141ABD830 + 1347) = *(_BYTE *)(qword_141ABD830 + 1363) ^ 1;
            return v4;
          }
          if ( (_DWORD)a2 == 1735419494 )
            return sub_14005BB10();
        }
        else
        {
          if ( (_DWORD)a2 == 1684825205 )
          {
            sub_1400393E0(a1: *(_QWORD *)(a1 + 352));
            return v4;
          }
          if ( (_DWORD)a2 == 1701077348 )
            return sub_14005F1A0(a1, a2: a3);
        }
        return (unsigned int)sub_140124190(a1: v7, a2: v6, a3: v5);
      }
      if ( (int)a2 > 1668051560 )
      {
        if ( (_DWORD)a2 == 1668051561 )
        {
          sub_14005C210(a1);
          return v4;
        }
        if ( (_DWORD)a2 == 1668052076 )
          return sub_14005A8F0(a1, a2: a3);
        if ( (_DWORD)a2 != 1668052083 )
          return (unsigned int)sub_140124190(a1: v7, a2: v6, a3: v5);
        sub_140048080(a1: v52);
        v20 = v52[0];
        if ( v52[0] != 0 )
        {
          sub_1407D8AB0(a1: v50, a2: 0x1418E2C24LL);
          sub_1407D19F0(a1: v20, a2: v49, a3: v50, a4: 3);
        }
        v21 = qword_141ABD830;
        sub_140051C40(a1: qword_141ABD830 + 1432);
        *(_BYTE *)(v21 + 1424) = 0;
        *(_BYTE *)(v21 + 1512) = 0;
LABEL_184:
        v34 = (void (__fastcall ***)(_QWORD, __int64))v52[0];
        if ( v52[0] == 0 || _InterlockedDecrement((volatile signed __int32 *)(v52[0] + 8LL)) != 0 )
          return v4;
        v35 = *v34;
        goto LABEL_235;
      }
      if ( (_DWORD)a2 == 1667658341 )
        return sub_140048810(a1: qword_141ABF5C0);
      if ( (_DWORD)a2 != 1667658354 )
      {
        if ( (_DWORD)a2 != 1667789417 )
          return (unsigned int)sub_140124190(a1: v7, a2: v6, a3: v5);
        goto LABEL_107;
      }
      LOBYTE(a2) = 1;
      if ( (unsigned __int8)sub_140049BB0(a1: qword_141ABF5C0, a2) != 0 )
        return sub_140049BB0(a1: qword_141ABF5C0, a2: 0);
    }
    else
    {
      if ( (int)a2 <= 1398173280 )
      {
        if ( (int)a2 > 1095135343 )
        {
          if ( (int)a2 > 1397321312 )
          {
            if ( (unsigned int)(a2 - 1397321313) <= 0xF )
            {
              v14 = 40965;
              if ( _bittest(&v14, a2 - 1397321313) )
                return v4;
            }
            return (unsigned int)sub_140124190(a1: v7, a2: v6, a3: v5);
          }
          if ( (_DWORD)a2 != 1095135344 )
          {
            if ( (_DWORD)a2 == 1128350551 )
              return sub_14005D6F0(a1);
            if ( (_DWORD)a2 == 1147356772 )
              return sub_140062F40();
            return (unsigned int)sub_140124190(a1: v7, a2: v6, a3: v5);
          }
          return sub_140062460(a1, a2: a3);
        }
        if ( (int)a2 > 1094996555 )
        {
          if ( (int)a2 > 1095133029 )
          {
            if ( (_DWORD)a2 != 1095133030 && (_DWORD)a2 != 1095135075 )
              return (unsigned int)sub_140124190(a1: v7, a2: v6, a3: v5);
            return sub_140062460(a1, a2: a3);
          }
          if ( (_DWORD)a2 != 1094996556 )
          {
            if ( (_DWORD)a2 != 1095131510 )
              return (unsigned int)sub_140124190(a1: v7, a2: v6, a3: v5);
            return sub_140062460(a1, a2: a3);
          }
          v17 = a3;
          LOBYTE(a3) = 1;
          LOBYTE(a4) = 1;
          return sub_14005C850(a1, a2: v17, a3, a4);
        }
        switch ( (_DWORD)a2 )
        {
          case 0x41444350:
            v17 = a3;
            a3 = 0;
            break;
          case 0x41444C47:
            v17 = a3;
            LOBYTE(a3) = 1;
            break;
          case 0x41445243:
            v17 = a3;
            a3 = 0;
            LOBYTE(a4) = 1;
            return sub_14005C850(a1, a2: v17, a3, a4);
          default:
            return (unsigned int)sub_140124190(a1: v7, a2: v6, a3: v5);
        }
        a4 = 0;
        return sub_14005C850(a1, a2: v17, a3, a4);
      }
      if ( (int)a2 <= 1633972843 )
      {
        if ( (unsigned int)(a2 - 1398173281) <= 0xF )
        {
          v12 = 40965;
          if ( _bittest(&v12, a2 - 1398173281) )
            return v4;
        }
        if ( (_DWORD)a2 == 1633907308 )
          return sub_14005E160(a1: v7);
        if ( (_DWORD)a2 == 1633972835 )
        {
          sub_14005E010(a1: v7);
          return v4;
        }
        return (unsigned int)sub_140124190(a1: v7, a2: v6, a3: v5);
      }
      if ( (int)a2 <= 1651209077 )
      {
        switch ( (_DWORD)a2 )
        {
          case 0x6164726C:
            return sub_14005D930(a1);
          case 0x6169726C:
            return sub_14005E410(a1);
          case 0x6176726C:
            return sub_14005E2E0(a1);
          default:
            break;
        }
        return (unsigned int)sub_140124190(a1: v7, a2: v6, a3: v5);
      }
      if ( (_DWORD)a2 == 1651209078 )
      {
        *(_BYTE *)(qword_141ABD830 + 1358) ^= 1u;
        return v4;
      }
      if ( (_DWORD)a2 == 1667460710 )
      {
        *(_BYTE *)(qword_141ABD830 + 1365) ^= 1u;
        return v4;
      }
      if ( (_DWORD)a2 != 1667657074 )
        return (unsigned int)sub_140124190(a1: v7, a2: v6, a3: v5);
      LOBYTE(a2) = 1;
      if ( (unsigned __int8)sub_14004AF40(a1: qword_141ABF5C0, a2) != 0 )
        return sub_14004AF40(a1: qword_141ABF5C0, a2: 0);
    }
    return 0;
  }
  if ( (int)a2 > 1919775339 )
  {
    if ( (int)a2 <= 1937142883 )
    {
      if ( (int)a2 <= 1936286578 )
      {
        if ( (int)a2 <= 1935895928 )
        {
          if ( (_DWORD)a2 == 1919775340 )
          {
            sub_14005E550(a1);
            return v4;
          }
          if ( (_DWORD)a2 == 1919970915 || (_DWORD)a2 == 1919970928 )
          {
            sub_140061B90(a1, a2: a3, a3: 0);
            return v4;
          }
          return (unsigned int)sub_140124190(a1: v7, a2: v6, a3: v5);
        }
        if ( (int)a2 <= 1936222322 )
        {
          if ( (_DWORD)a2 == 1935895929 )
          {
            *(_BYTE *)(qword_141ABD830 + 1350) ^= 1u;
            return v4;
          }
          if ( (_DWORD)a2 == 1935958646 )
          {
            *(_BYTE *)(qword_141ABD830 + 1356) ^= 1u;
            LOBYTE(a3) = -1;
            sub_140016B80(a1: qword_141ABF5C0, a2: 0, a3);
            sub_14005A8F0(a1: v7, a2: v5);
            return v4;
          }
          return (unsigned int)sub_140124190(a1: v7, a2: v6, a3: v5);
        }
        if ( (_DWORD)a2 == 1936222323 )
        {
          *(_BYTE *)(qword_141ABD830 + 1367) ^= 1u;
          return v4;
        }
        if ( (_DWORD)a2 != 1936225139 )
          return (unsigned int)sub_140124190(a1: v7, a2: v6, a3: v5);
        if ( *(_BYTE *)(qword_141ABD830 + 1356) != 0 )
          LOBYTE(a2) = *(_BYTE *)(qword_141ABD830 + 1357) == 0;
        else
          a2 = 0;
        sub_140094350(a1: qword_141ABD830, a2);
        sub_14005A740(a1: v7);
        if ( (unsigned __int8)sub_140205850(a1: v7 + 400, a2: v7, a3: 0) == 0 )
          return v4;
        a1 = *(_QWORD *)(v7 + 400);
        v19 = 1919247986;
LABEL_239:
        sub_140147750(a1, a2: v19, a3: 0);
        return v4;
      }
      if ( (int)a2 <= 1937138533 )
      {
        if ( (_DWORD)a2 == 1936286579 )
        {
          *(_BYTE *)(qword_141ABD830 + 1344) ^= 1u;
          return v4;
        }
        if ( (_DWORD)a2 == 1936548962 )
        {
          *(_BYTE *)(qword_141ABD830 + 1370) ^= 1u;
          return v4;
        }
        if ( (_DWORD)a2 != 1936738628 )
          return (unsigned int)sub_140124190(a1: v7, a2: v6, a3: v5);
        *(_BYTE *)(qword_141ABD830 + 1351) ^= 1u;
        v19 = 1919705960;
        goto LABEL_239;
      }
      if ( (int)a2 > 1937139314 )
      {
        if ( (_DWORD)a2 == 1937139315 )
          return v4;
        if ( (_DWORD)a2 == 1937142371 )
        {
          sub_140146740(a1: v52, a2: 1818518374, a3: 0);
          v25 = sub_140835850(a1: v5, a2: 1952807028);
          sub_1408351C0(a1: v52, a2: 1936091500, a3: v25);
          sub_1407D8AB0(a1: v49, a2: 0x1418E2C24LL);
          v26 = sub_140179440(a1: v49);
          sub_14083D970(a1: v50, a2: v26);
          sub_140835380(a1: v52, a2: 1937013104, a3: v50);
          sub_14083D320(a1: v50);
          v4 = sub_140147670(a1: v7, a2: v52);
          sub_140833970(a1: v52);
          return v4;
        }
        return (unsigned int)sub_140124190(a1: v7, a2: v6, a3: v5);
      }
      if ( (_DWORD)a2 != 1937138534 )
      {
        if ( (_DWORD)a2 == 1937139299 )
          return v4;
        return (unsigned int)sub_140124190(a1: v7, a2: v6, a3: v5);
      }
      v28 = sub_140835850(a1: a3, a2: 1936093036);
      v29 = sub_140843600();
      sub_1408436F0(a1: v29, a2: v52, a3: v28);
      v30 = sub_140835850(a1: v5, a2: 1936091500);
      sub_14083E100(a1: v30, a2: v49);
      sub_1407D5F40(a1: v50, a2: v49);
      sub_140808B00(a1: v49);
      v31 = sub_140835850(a1: v5, a2: 1937013104);
      sub_14083E100(a1: v31, a2: &v51);
      sub_1407D8AC0(a1: v49, a2: &v51);
      sub_140808B00(a1: &v51);
      v32 = sub_140835E00(a1: v5, a2: 1684152352);
      v33 = qword_141ABD830;
      v53 = v52[0];
      if ( v52[0] != 0 )
        _InterlockedIncrement((volatile signed __int32 *)(v52[0] + 8LL));
      sub_140097B50(a1: v33, a2: &v53, a3: v50, a4: v49, a5: v32, a6: 0);
      sub_140014610(a1: qword_141ABF5C0, a2: 0);
      sub_140147750(a1: v7, a2: 1919705960, a3: 0);
      sub_140808B00(a1: v50);
      goto LABEL_184;
    }
    if ( (int)a2 > 1970303605 )
    {
      if ( (int)a2 <= 1970499680 )
      {
        if ( (_DWORD)a2 != 1970303606 )
        {
          if ( (_DWORD)a2 == 1970304884 )
          {
            *(_BYTE *)(qword_141ABD830 + 1368) ^= 1u;
            return v4;
          }
          if ( (_DWORD)a2 == 1970496107 )
          {
            *(_BYTE *)(qword_141ABD830 + 1376) ^= 1u;
            return v4;
          }
          return (unsigned int)sub_140124190(a1: v7, a2: v6, a3: v5);
        }
      }
      else
      {
        if ( (int)a2 > 1970501486 )
        {
          if ( (_DWORD)a2 == 1970501487 )
          {
            *(_BYTE *)(qword_141ABD830 + 1349) ^= 1u;
            return v4;
          }
          if ( (_DWORD)a2 == 1986815608 )
          {
            *(_BYTE *)(qword_141ABD830 + 1366) ^= 1u;
            return v4;
          }
          return (unsigned int)sub_140124190(a1: v7, a2: v6, a3: v5);
        }
        if ( (_DWORD)a2 != 1970499681 )
        {
          if ( (_DWORD)a2 == 1970499949 )
          {
            *(_BYTE *)(qword_141ABD830 + 1371) ^= 1u;
            return v4;
          }
          return (unsigned int)sub_140124190(a1: v7, a2: v6, a3: v5);
        }
      }
      return sub_14005A8F0(a1, a2: a3);
    }
    if ( (int)a2 > 1953718637 )
    {
      if ( (int)a2 > 1953722987 )
      {
        if ( (_DWORD)a2 == 1953722988 )
        {
          sub_14005E6D0(a1);
          return v4;
        }
        if ( (_DWORD)a2 == 1969646952 )
        {
          *(_BYTE *)(qword_141ABD830 + 1363) ^= 1u;
          return v4;
        }
      }
      else if ( (_DWORD)a2 == 1953718638 || (_DWORD)a2 == 1953718642 )
      {
        sub_14005ED20(a1, a2: a3);
        return v4;
      }
      return (unsigned int)sub_140124190(a1: v7, a2: v6, a3: v5);
    }
    if ( (_DWORD)a2 == 1937142884 || (_DWORD)a2 == 1937142899 )
    {
      LOBYTE(a2) = (_DWORD)a2 == 1937142884;
      sub_140063730(a1, a2);
      return v4;
    }
    if ( (_DWORD)a2 != 1937337971 )
      return (unsigned int)sub_140124190(a1: v7, a2: v6, a3: v5);
LABEL_107:
    sub_14005A8F0(a1, a2: a3);
    return (unsigned int)sub_140124190(a1: v7, a2: v6, a3: v5);
  }
  if ( (int)a2 > 1919247985 )
  {
    if ( (int)a2 <= 1919643234 )
    {
      if ( (int)a2 > 1919511136 )
      {
        if ( (unsigned int)(a2 - 1919511137) <= 0xF )
        {
          v15 = 40965;
          if ( _bittest(&v15, a2 - 1919511137) )
          {
            sub_1400627B0(a1: v7, a2: a3);
            return v4;
          }
        }
        return (unsigned int)sub_140124190(a1: v7, a2: v6, a3: v5);
      }
      if ( (_DWORD)a2 == 1919247986 )
      {
        v37 = (_QWORD *)(a1 + 400);
        if ( (unsigned __int8)sub_140205850(a1: a1 + 400, a2: a1, a3: 0) != 0 )
          sub_140147750(a1: *v37, a2: 1919247986, a3: 0);
        return (unsigned int)sub_140124190(a1: v7, a2: v6, a3: v5);
      }
      if ( (_DWORD)a2 == 1919251060 )
      {
        sub_14005F5A0(a1, a2: a3);
        return v4;
      }
      if ( (_DWORD)a2 != 1919316579 )
        return (unsigned int)sub_140124190(a1: v7, a2: v6, a3: v5);
      return sub_14005A8F0(a1, a2: a3);
    }
    if ( (unsigned int)(a2 - 1919709025) <= 0xF )
    {
      v16 = 40965;
      if ( _bittest(&v16, a2 - 1919709025) )
      {
        sub_140060850(a1: v7, a2: a3);
        return v4;
      }
    }
    if ( (unsigned int)(a2 - 1919643235) <= 0xD )
    {
      v11 = 10241;
      if ( _bittest(&v11, a2 - 1919643235) )
      {
        sub_1400615D0(a1: v7, a2: a3);
        return v4;
      }
    }
    if ( (_DWORD)a2 == 1919705960 )
    {
      sub_140146740(a1: v52, a2: 1919705971, a3: 0);
      if ( (unsigned __int8)sub_1408357E0(a1: v5, a2: 1396854857) != 0 )
      {
        v27 = sub_140835850(a1: v5, a2: 1396854857);
        sub_1408351C0(a1: v52, a2: 1396854857, a3: v27);
      }
      sub_14005A8F0(a1: v7, a2: v52);
      if ( (unsigned __int8)sub_140205850(a1: v7 + 400, a2: v7, a3: 0) != 0 )
        sub_140147750(a1: *(_QWORD *)(v7 + 400), a2: 1919247986, a3: 0);
      sub_140833970(a1: v52);
    }
    return (unsigned int)sub_140124190(a1: v7, a2: v6, a3: v5);
  }
  if ( (int)a2 > 1852992608 )
  {
    if ( (int)a2 > 1919053408 )
    {
      if ( (unsigned int)(a2 - 1919053409) <= 0xF )
      {
        v13 = 40965;
        if ( _bittest(&v13, a2 - 1919053409) )
        {
          sub_140060EC0(a1: v7, a2: a3);
          return v4;
        }
      }
      return (unsigned int)sub_140124190(a1: v7, a2: v6, a3: v5);
    }
    if ( (_DWORD)a2 != 1852992609 )
    {
      if ( (_DWORD)a2 == 1917873763 || (_DWORD)a2 == 1917873776 )
      {
        LOBYTE(v4) = 1;
        v18 = a3;
        LOBYTE(a3) = 1;
        sub_140061B90(a1, a2: v18, a3);
        return v4;
      }
      return (unsigned int)sub_140124190(a1: v7, a2: v6, a3: v5);
    }
    return sub_14005A8F0(a1, a2: a3);
  }
  v8 = (unsigned int)(a2 - 1835823171);
  if ( (unsigned int)v8 > 0x2D || (v9 = 0x280140002801LL, !_bittest64(&v9, v8)) )
  {
    if ( (_DWORD)a2 == 1836413033 )
      return sub_14005F8C0(a1: v7, a2: a3);
    return (unsigned int)sub_140124190(a1: v7, a2: v6, a3: v5);
  }
  sub_14005FF60(a1: v7, a2: a3);
  return v4;
}
