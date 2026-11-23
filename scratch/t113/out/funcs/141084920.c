__int64 __fastcall sub_141084920(__int64 a1, int a2, _QWORD *a3)
{
  __int64 v3; // rdi
  __int64 v7; // rdx
  __int64 v8; // rcx
  unsigned __int64 v9; // rax
  __int64 v10; // rcx
  unsigned __int64 v11; // rax
  __int64 v12; // rcx
  unsigned __int64 v13; // rax
  int v14; // ecx
  unsigned __int64 v15; // rax
  __int64 v16; // rcx
  __int64 v17; // rax
  __int64 v18; // rax
  __int64 v19; // rsi
  unsigned __int64 v20; // rax
  __int64 v21; // rcx
  unsigned int v22; // eax
  int v23; // ecx
  int v24; // ecx
  unsigned __int64 v25; // rax
  __int64 v26; // rcx
  unsigned __int64 v27; // rax
  __int64 v28; // rcx
  int v29; // ecx
  int v30; // ecx
  __int64 v31; // rcx
  int v32; // ecx
  unsigned int v33; // eax
  __int64 v35; // rax
  __int64 v36; // rax
  __int64 v37; // rsi
  __int64 v38; // rax
  __int64 v39; // rax
  __int64 **v40; // rcx
  __int64 *v41; // rdx
  __int64 *v42; // rdi
  __int64 v43; // rcx
  __int64 v44; // rax
  __int64 **v45; // rcx
  __int64 *v46; // rdx
  __int64 *v47; // rdi
  unsigned int v48; // eax
  unsigned __int64 v49; // rax
  unsigned int v50; // eax
  __int64 v51; // rax
  int v52; // ebx
  __int64 v53; // rdx
  __int64 v54; // rcx
  int v55; // r15d
  int v56; // eax
  __int64 v57; // rax
  __int64 v58; // rdx
  __int64 v59; // rcx
  __int64 v60; // rax
  int v61; // esi
  __int64 v62; // rdx
  __int64 v63; // rcx
  __int64 v64; // rax
  __int64 v65; // rdx
  __int64 v66; // rcx
  __int64 v67; // rax
  __int64 v68; // rdx
  __int64 v69; // rcx
  __int64 v70; // rax
  __int64 v71; // rdx
  __int64 v72; // rcx
  __int64 v73; // rax
  int v74; // r8d
  __int64 v75; // rax
  __int64 v76; // rax
  __int64 v77; // rax
  bool v78; // zf
  _QWORD v79[2]; // [rsp+80h] [rbp+0h] BYREF
  __int64 v80; // [rsp+90h] [rbp+10h] BYREF
  _QWORD v81[3]; // [rsp+98h] [rbp+18h] BYREF
  __int64 *v82; // [rsp+B0h] [rbp+30h] BYREF
  _QWORD *v83; // [rsp+B8h] [rbp+38h]
  __int64 v84; // [rsp+C0h] [rbp+40h] BYREF
  int v85; // [rsp+C8h] [rbp+48h]
  __int64 v86; // [rsp+D0h] [rbp+50h]

  v86 = -2;
  if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)qword_141B5F278 + 32LL))(qword_141B5F278) == 0 )
  {
    LOBYTE(v3) = 1;
    if ( (*(unsigned __int8 (__fastcall **)(__int64, __int64, _QWORD, _QWORD *))(*(_QWORD *)qword_141B5F278 + 72LL))(
           qword_141B5F278,
           a1,
           (unsigned int)a2,
           a3) != 0 )
      return (unsigned int)v3;
  }
  LOBYTE(v3) = 1;
  if ( a2 <= 1346794597 )
  {
    if ( a2 > 1346790978 )
    {
      if ( a2 <= 1346792514 )
      {
        if ( a2 > 1346791746 )
        {
          v27 = (unsigned int)(a2 - 1346791747);
          if ( (unsigned int)v27 > 0x2A || (v28 = 0x40180000001LL, !_bittest64(&v28, v27)) )
          {
            if ( a2 != 1346792047 )
              return sub_140FE2700(a1, (unsigned int)a2, a3);
          }
          goto LABEL_144;
        }
        v15 = (unsigned int)(a2 - 1346790979);
        if ( (unsigned int)v15 <= 0x2F )
        {
          v16 = 0x80000000002BLL;
          if ( _bittest64(&v16, v15) )
            goto LABEL_144;
        }
        v11 = (unsigned int)(a2 - 1346791235);
        if ( (unsigned int)v11 <= 0x2B )
        {
          v12 = 0x80180000001LL;
LABEL_37:
          if ( !_bittest64(&v12, v11) )
            return sub_140FE2700(a1, (unsigned int)a2, a3);
LABEL_144:
          v39 = *(int *)(a1 + 8);
          if ( (*(_BYTE *)(qword_141B5FE08 + 90) & 4) != 0 )
            v39 = a1;
          v40 = *(__int64 ***)(qword_141B60110 + 128);
          v41 = *v40;
          v42 = v40[1];
          if ( *v40 != v42 )
          {
            do
            {
              v43 = *v41;
              if ( *(_QWORD *)(*v41 + 72) == v39 )
                return sub_141194740(v43, (unsigned int)a2, a3);
              ++v41;
            }
            while ( v41 != v42 );
          }
          LODWORD(v3) = 0;
          if ( sub_140F7CDA0((unsigned int)&qword_141B5FDA8, a1, 0, 0, 0x1418761ECLL, 0, -1, 3, 0, 1, 0, 6, 0, 0, 0) != 0 )
          {
            v44 = *(int *)(a1 + 8);
            if ( (*(_BYTE *)(qword_141B5FE08 + 90) & 4) != 0 )
              v44 = a1;
            v45 = *(__int64 ***)(qword_141B60110 + 128);
            v46 = *v45;
            v47 = v45[1];
            if ( *v45 != v47 )
            {
              while ( 1 )
              {
                v43 = *v46;
                if ( *(_QWORD *)(*v46 + 72) == v44 )
                  return sub_141194740(v43, (unsigned int)a2, a3);
                if ( ++v46 == v47 )
                  goto LABEL_155;
              }
            }
            goto LABEL_155;
          }
          return (unsigned int)v3;
        }
      }
      else
      {
        if ( a2 > 1346793074 )
        {
          if ( a2 > 1346794083 )
          {
            if ( a2 != 1346794084 && a2 != 1346794086 )
              return sub_140FE2700(a1, (unsigned int)a2, a3);
          }
          else
          {
            v20 = (unsigned int)(a2 - 1346793539);
            if ( (unsigned int)v20 > 0x2F || (v21 = 0x844100000001LL, !_bittest64(&v21, v20)) )
            {
              if ( a2 != 1346793075 )
                return sub_140FE2700(a1, (unsigned int)a2, a3);
            }
          }
          goto LABEL_144;
        }
        v9 = (unsigned int)(a2 - 1346792771);
        if ( (unsigned int)v9 <= 0x2A )
        {
          v10 = 0x46100000001LL;
          if ( _bittest64(&v10, v9) )
            goto LABEL_144;
        }
        v11 = (unsigned int)(a2 - 1346792515);
        if ( (unsigned int)v11 <= 0x2A )
        {
          v12 = 0x40100000001LL;
          goto LABEL_37;
        }
      }
      return sub_140FE2700(a1, (unsigned int)a2, a3);
    }
    if ( a2 > 1346786392 )
    {
      if ( a2 <= 1346790241 )
      {
        if ( a2 > 1346789743 )
        {
          if ( a2 != 1346789744 && a2 != 1346789955 && a2 != 1346789986 )
            return sub_140FE2700(a1, (unsigned int)a2, a3);
        }
        else if ( a2 != 1346786393 && a2 != 1346787139 && a2 != 1346789730 )
        {
          return sub_140FE2700(a1, (unsigned int)a2, a3);
        }
      }
      else if ( (unsigned int)(a2 - 1346790242) > 0x11 || (v32 = 132097, !_bittest(&v32, a2 - 1346790242)) )
      {
        if ( (unsigned int)(a2 - 1346790755) > 0xB || (v14 = 2051, !_bittest(&v14, a2 - 1346790755)) )
        {
          if ( a2 != 1346790516 )
            return sub_140FE2700(a1, (unsigned int)a2, a3);
        }
      }
      goto LABEL_144;
    }
    if ( a2 > 1346783057 )
    {
      if ( a2 <= 1346786117 )
      {
        if ( a2 != 1346783058 && a2 != 1346784327 )
          return sub_140FE2700(a1, (unsigned int)a2, a3);
      }
      else
      {
        v25 = (unsigned int)(a2 - 1346786118);
        if ( (unsigned int)v25 > 0x2A || (v26 = 0x44000000001LL, !_bittest64(&v26, v25)) )
        {
          if ( a2 != 1346786375 )
            return sub_140FE2700(a1, (unsigned int)a2, a3);
        }
      }
      goto LABEL_144;
    }
    if ( a2 > 1346777423 )
    {
      if ( a2 != 1346777424 && a2 != 1346782040 && a2 != 1346782061 )
        return sub_140FE2700(a1, (unsigned int)a2, a3);
      goto LABEL_144;
    }
    if ( a2 == 1145392197 )
    {
      sub_1410864B0(a1);
      return (unsigned int)v3;
    }
    if ( a2 != 1346585666 )
    {
      if ( a2 != 1346777409 )
        return sub_140FE2700(a1, (unsigned int)a2, a3);
      goto LABEL_144;
    }
    v49 = *(_QWORD *)(a1 + 24) & 0xFFFFFFFFFFFFFFEFuLL
        | (16LL * (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 48LL))(*a3, a3));
LABEL_167:
    *(_QWORD *)(a1 + 24) = v49;
    return (unsigned int)v3;
  }
  if ( a2 <= 1347187555 )
  {
    if ( a2 <= 1347183467 )
    {
      if ( a2 <= 1347174722 )
      {
        if ( (unsigned int)(a2 - 1346795361) > 0xF || (v29 = 33025, !_bittest(&v29, a2 - 1346795361)) )
        {
          if ( a2 != 1346794598 && a2 != 1346795600 )
            return sub_140FE2700(a1, (unsigned int)a2, a3);
        }
        goto LABEL_144;
      }
      if ( a2 > 1347176043 )
      {
        if ( a2 > 1347178054 )
        {
          if ( a2 != 1347178055 && a2 != 1347183218 )
            return sub_140FE2700(a1, (unsigned int)a2, a3);
        }
        else if ( a2 != 1347176044 )
        {
          if ( a2 != 1347176803 )
            return sub_140FE2700(a1, (unsigned int)a2, a3);
          goto LABEL_144;
        }
        return sub_141086B00(a1, (unsigned int)a2, a3);
      }
      v22 = a2 - 1347174723;
      if ( (unsigned int)(a2 - 1347174723) > 0x11 )
        return sub_140FE2700(a1, (unsigned int)a2, a3);
      v23 = 196609;
    }
    else
    {
      if ( a2 > 1347184962 )
      {
        if ( a2 > 1347186021 )
        {
          if ( (unsigned int)(a2 - 1347186530) >= 2 && a2 != 1347186022 && a2 != 1347186759 )
            return sub_140FE2700(a1, (unsigned int)a2, a3);
        }
        else if ( a2 > 1347185004 )
        {
          if ( a2 == 1347185005 )
            goto LABEL_144;
          if ( a2 != 1347186019 )
            return sub_140FE2700(a1, (unsigned int)a2, a3);
        }
        else
        {
          if ( a2 == 1347184963 )
            goto LABEL_144;
          if ( a2 != 1347184995 )
            return sub_140FE2700(a1, (unsigned int)a2, a3);
        }
        return sub_141086B00(a1, (unsigned int)a2, a3);
      }
      if ( a2 > 1347183971 )
      {
        if ( a2 != 1347183972 && a2 != 1347184226 && a2 != 1347184236 )
          return sub_140FE2700(a1, (unsigned int)a2, a3);
        return sub_141086B00(a1, (unsigned int)a2, a3);
      }
      v22 = a2 - 1347183468;
      if ( (unsigned int)(a2 - 1347183468) > 8 )
        return sub_140FE2700(a1, (unsigned int)a2, a3);
      v23 = 323;
    }
    if ( !_bittest(&v23, v22) )
      return sub_140FE2700(a1, (unsigned int)a2, a3);
    return sub_141086B00(a1, (unsigned int)a2, a3);
  }
  if ( a2 <= 1348101953 )
  {
    if ( a2 > 1347905345 )
    {
      if ( (unsigned int)(a2 - 1347905346) > 5 || (v30 = 35, !_bittest(&v30, a2 - 1347905346)) )
      {
        v13 = (unsigned int)(a2 - 1347905859);
        if ( (unsigned int)v13 > 0x2A || (v31 = 0x40100000001LL, !_bittest64(&v31, v13)) )
        {
          if ( (unsigned int)(a2 - 1348036417) >= 3 )
            return sub_140FE2700(a1, (unsigned int)a2, a3);
        }
      }
      goto LABEL_144;
    }
    if ( a2 > 1347188582 )
    {
      if ( a2 == 1347188583 )
      {
        v51 = sub_14083D4F0(v8, v7);
        v83 = nullptr;
        v82 = (__int64 *)(v51 + 8);
        if ( (*(unsigned __int8 (__fastcall **)(__int64, __int64, __int64 **))(*(_QWORD *)a1 + 16LL))(
               a1,
               1348695911,
               &v82) != 0
          && (v52 = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(*v82 + 64))(v82, &v82)) > 0 )
        {
          v55 = -1;
          if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) != 0 )
          {
            v56 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
            v54 = (unsigned int)(4 * v52);
            if ( v56 < (int)v54 )
              v54 = (unsigned int)v56;
            if ( v56 <= 0 )
              v54 = (unsigned int)v56;
            if ( (int)v54 >= 0 )
            {
              v53 = (unsigned int)((100 * (int)v54) >> 31);
              LODWORD(v53) = 100 * (int)v54 % v52;
              v55 = 100 * (int)v54 / v52;
            }
          }
          v57 = sub_14083D4F0(v54, v53);
          v79[1] = 0;
          v79[0] = v57 + 8;
          (*(void (__fastcall **)(__int64, __int64, _QWORD *))(*(_QWORD *)a1 + 16LL))(a1, 1347188579, v79);
          sub_1407C9510(&v80);
          v60 = sub_14083D4F0(v59, v58);
          v85 = 1;
          v84 = v60 + 40;
          sub_140833EB0(&v80, 1685353593, &v84);
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v84 + 16LL))(v84, &v84);
          v61 = *(_DWORD *)(a1 + 12);
          v64 = sub_14083D4F0(v63, v62);
          v85 = v61;
          v84 = v64 + 40;
          sub_140833EB0(&v80, 1685417577, &v84);
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v84 + 16LL))(v84, &v84);
          v67 = sub_14083D4F0(v66, v65);
          v85 = 1347188579;
          v84 = v67 + 56;
          sub_140833EB0(&v80, 1886549113, &v84);
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v84 + 16LL))(v84, &v84);
          v70 = sub_14083D4F0(v69, v68);
          LOBYTE(v85) = 0;
          v84 = v70 + 24;
          sub_140833EB0(&v80, 1230193478, &v84);
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v84 + 16LL))(v84, &v84);
          v73 = sub_14083D4F0(v72, v71);
          v85 = v55;
          v84 = v73 + 40;
          sub_140833EB0(&v80, 1853322860, &v84);
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v84 + 16LL))(v84, &v84);
          sub_140835A40(&v80, 1868854892, v79);
          LOBYTE(v74) = 1;
          LODWORD(v3) = sub_140F47AD0(
                          (unsigned int)&qword_141B5FDA8,
                          (unsigned int)&v80,
                          v74,
                          0,
                          1,
                          0,
                          1,
                          0,
                          0,
                          1,
                          0,
                          0);
          sub_140833970(&v80);
          (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v79[0] + 16LL))(v79[0], v79);
        }
        else
        {
          LODWORD(v3) = 0;
        }
        (*(void (__fastcall **)(__int64 *, __int64 **))(*v82 + 16))(v82, &v82);
      }
      else if ( a2 == 1347449684 )
      {
        v80 = a1;
        sub_1415D2310(v81, a1);
        v82 = &v80;
        v83 = v81;
        LODWORD(v3) = sub_1410B5F70(&v82, a3);
        if ( v81[0] != 0 )
          sub_1407E4890(qword_141ABD470, v81[0], v81[2] - v81[0]);
      }
      else
      {
        LOBYTE(v3) = 1;
        if ( a2 != 1347643470 )
          return sub_140FE2700(a1, (unsigned int)a2, a3);
      }
      return (unsigned int)v3;
    }
    if ( a2 != 1347187556 && a2 != 1347187566 && a2 != 1347188579 )
      return sub_140FE2700(a1, (unsigned int)a2, a3);
    return sub_141086B00(a1, (unsigned int)a2, a3);
  }
  if ( a2 > 1348887137 )
  {
    if ( a2 > 1349674342 )
    {
      if ( a2 > 1349810543 )
      {
        if ( a2 != 1381125700 )
        {
          if ( a2 == 1349810544 )
          {
            v48 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
            return sub_141085700(a1, v48);
          }
          return sub_140FE2700(a1, (unsigned int)a2, a3);
        }
        if ( (*(_BYTE *)(a1 + 25) & 4) == 0 && (unsigned __int8)sub_140835E00(&qword_141B60C30, 1198679666) == 0 )
        {
          *(_BYTE *)(a1 + 25) |= 4u;
          if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)qword_141B5AD60 + 32LL))(qword_141B5AD60) != 0 )
          {
            if ( *(_BYTE *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex) + 8LL) == 0 )
              sub_141751038();
            sub_140F7CF50(
              &qword_141B5FDA8,
              a1,
              *((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex) + 320LL,
              0);
            LOBYTE(v3) = 1;
          }
        }
        return (unsigned int)v3;
      }
      if ( a2 != 1349674343 )
      {
        if ( a2 == 1349740114 )
        {
          v17 = sub_140FE8230();
          v18 = sub_141086700(a1, v17);
          if ( v18 != 0 )
          {
            v19 = v18;
            if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 48LL))(*a3, a3) != 0 )
            {
              if ( (unsigned __int8)sub_140EF7550(v19) != 0 )
                *(_BYTE *)(v19 + 79) |= 0x20u;
            }
            else
            {
              v78 = (*(_BYTE *)(v19 + 79) & 0xDF) == 0;
              *(_BYTE *)(v19 + 79) &= ~0x20u;
              if ( v78 )
                *(_DWORD *)(v19 + 72) = 124518401;
              *(_BYTE *)(v19 + 80) = 0;
              LOBYTE(v3) = 1;
            }
          }
          return (unsigned int)v3;
        }
        return sub_140FE2700(a1, (unsigned int)a2, a3);
      }
      v49 = (*(_QWORD *)(a1 + 24) & 0xFFFFFFFFFFFFFFF7uLL)
          + 8LL * (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 48LL))(*a3, a3);
      goto LABEL_167;
    }
    if ( a2 != 1348887138 )
    {
      if ( a2 == 1349084773 )
      {
        v50 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 48LL))(*a3, a3);
        sub_1410865A0(a1, v50);
        return (unsigned int)v3;
      }
      if ( a2 == 1349416051 )
      {
        v33 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
        sub_141086600(a1, v33);
        return (unsigned int)v3;
      }
      return sub_140FE2700(a1, (unsigned int)a2, a3);
    }
    return sub_141086B00(a1, (unsigned int)a2, a3);
  }
  if ( a2 <= 1348690539 )
  {
    if ( (unsigned int)(a2 - 1348101954) > 5 )
      return sub_140FE2700(a1, (unsigned int)a2, a3);
    v24 = 35;
    if ( !_bittest(&v24, a2 - 1348101954) )
      return sub_140FE2700(a1, (unsigned int)a2, a3);
    goto LABEL_144;
  }
  if ( a2 != 1348690540 )
  {
    if ( a2 == 1348696131 )
    {
      v3 = sub_141086760(a1);
      if ( v3 == 0 )
      {
        v77 = qword_141B60448;
        if ( qword_141B60448 == qword_141B60450 )
          goto LABEL_155;
        while ( 1 )
        {
          v3 = *(_QWORD *)v77;
          if ( *(_QWORD *)(*(_QWORD *)v77 + 8LL) == a1 )
            break;
          v77 += 8;
          LODWORD(v3) = 0;
          if ( v77 == qword_141B60450 )
            return (unsigned int)v3;
        }
      }
      v76 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *, _QWORD))(*(_QWORD *)*a3 + 176LL))(*a3, a3, 0);
      sub_1407EAF60(v3, v76);
      LOBYTE(v3) = 1;
      return (unsigned int)v3;
    }
    if ( a2 != 1348696143 )
      return sub_140FE2700(a1, (unsigned int)a2, a3);
    v35 = sub_141086760(a1);
    v36 = (*(__int64 (__fastcall **)(__int64, __int64))(*(_QWORD *)a1 + 952LL))(a1, v35);
    if ( v36 != 0 )
    {
      v37 = v36;
      v38 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *, _QWORD))(*(_QWORD *)*a3 + 176LL))(*a3, a3, 0);
      sub_1407EAF60(v37, v38);
      return (unsigned int)v3;
    }
LABEL_155:
    LODWORD(v3) = 0;
    return (unsigned int)v3;
  }
  v75 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)a1 + 1032LL))(a1);
  if ( v75 == 0 )
    goto LABEL_155;
  return (*(__int64 (__fastcall **)(__int64, __int64, _QWORD *))(*(_QWORD *)v75 + 24LL))(v75, 1130586732, a3);
}
