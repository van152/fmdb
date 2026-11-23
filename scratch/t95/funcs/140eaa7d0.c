__int64 __fastcall sub_140EAA7D0(__int64 *a1, __int64 **a2)
{
  __int64 *v2; // r15
  char v5; // al
  __int64 *v6; // rcx
  __int64 v7; // rbp
  __int64 *v8; // rbx
  __int64 v9; // rax
  __int64 v10; // rcx
  __int64 v11; // rdx
  __int64 v12; // r12
  __int64 v13; // r12
  __int64 v14; // rax
  __int64 v15; // rbx
  _QWORD *v16; // rsi
  __int64 v17; // rax
  __int64 v18; // rsi
  __int64 k; // rdi
  __int64 v20; // rax
  unsigned __int64 v21; // rax
  __int64 v22; // r12
  __int64 m; // rdi
  __int64 *v24; // rsi
  __int64 v25; // rax
  __int64 v26; // rbx
  _QWORD *v27; // rsi
  __int64 v28; // rbp
  __int64 v29; // rbp
  __int64 v30; // r14
  __int64 *v31; // r8
  __int64 v32; // rcx
  __int64 v33; // rax
  __int64 *v34; // rdx
  _QWORD **v35; // r14
  __int64 v36; // rax
  __int64 v37; // rcx
  __int64 *v38; // rdx
  __int64 v39; // rcx
  __int64 v40; // rdx
  __int64 *v41; // rax
  __int64 v42; // r12
  __int64 v43; // r12
  __int64 v44; // rax
  __int64 v45; // rbx
  _QWORD *v46; // rsi
  __int64 v47; // rax
  __int64 v48; // rsi
  __int64 j; // rdi
  __int64 v50; // rax
  __int64 v51; // rcx
  __int64 *v52; // rbx
  int v53; // eax
  __int64 v54; // rsi
  __int64 v55; // rbp
  __int64 v56; // rcx
  __int64 *v57; // rdx
  __int64 v58; // rax
  __int64 *v59; // rbx
  _QWORD **v60; // r14
  int v61; // eax
  __int64 v62; // rax
  __int64 v63; // rsi
  _QWORD *v64; // rbx
  __int64 v65; // rax
  __int64 v66; // r14
  __int64 i; // rbx
  __int64 v69; // rsi
  _QWORD *v70; // rbx
  __int64 v71; // rdi
  __int64 v72; // rdi
  __int64 v73; // rbp
  __int64 *v74; // r8
  unsigned int v75; // eax
  _QWORD *v76; // [rsp+20h] [rbp-48h]

  v5 = (*(__int64 (__fastcall **)(__int64 *))(**a2 + 8))(*a2);
  v6 = *a2;
  v7 = **a2;
  if ( v5 == 10 )
  {
    LODWORD(v2) = 0;
    v8 = (__int64 *)(*(__int64 (__fastcall **)(__int64 *, __int64 **, _QWORD))(v7 + 176))(v6, a2, 0);
    v9 = *v8;
    v10 = v8[1];
    if ( *v8 == v10 )
      return (unsigned int)v2;
    v11 = *v8;
    while ( *(_DWORD *)v11 != 1819504496 )
    {
      v11 += 16;
      if ( v11 == v10 )
        goto LABEL_105;
    }
    if ( v11 != v10 && *(_QWORD *)(v11 + 8) != 0 )
    {
      v34 = nullptr;
      while ( *(_DWORD *)v9 != 1819504496 )
      {
        v9 += 16;
        if ( v9 == v10 )
          goto LABEL_48;
      }
      if ( v9 == v10 )
        v34 = nullptr;
      else
        v34 = *(__int64 **)(v9 + 8);
LABEL_48:
      v2 = &qword_141B5A4A0;
      if ( v34 == nullptr )
        v34 = &qword_141B5A4A0;
      switch ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)*v34 + 64LL))(*v34) )
      {
        case 0u:
          LOBYTE(v2) = sub_14152B6C0(*a1) != 0;
          return (unsigned int)v2;
        case 1u:
          v35 = (_QWORD **)(a1 + 1);
          v36 = *v8;
          v37 = v8[1];
          v38 = nullptr;
          if ( *v8 != v37 )
          {
            while ( *(_DWORD *)v36 != 1869379180 )
            {
              v36 += 16;
              if ( v36 == v37 )
                goto LABEL_82;
            }
            if ( v36 == v37 )
              v38 = nullptr;
            else
              v38 = *(__int64 **)(v36 + 8);
          }
LABEL_82:
          if ( v38 == nullptr )
            v38 = &qword_141B5A4A0;
          v53 = sub_140EAAE10(v35, v38);
          if ( v53 < 0 )
            goto LABEL_105;
          v54 = *(_QWORD *)(**v35 + 8LL * (unsigned int)v53);
          if ( v54 == 0 )
            goto LABEL_105;
          v55 = *v8;
          v56 = v8[1];
          v57 = nullptr;
          if ( *v8 == v56 )
          {
            v59 = &qword_141B5A4A0;
          }
          else
          {
            v58 = *v8;
            while ( *(_DWORD *)v58 != 1986096245 )
            {
              v58 += 16;
              if ( v58 == v56 )
                goto LABEL_118;
            }
            if ( v58 == v56 )
              v57 = nullptr;
            else
              v57 = *(__int64 **)(v58 + 8);
LABEL_118:
            v59 = &qword_141B5A4A0;
            if ( v57 != nullptr )
              v59 = v57;
            v57 = nullptr;
            while ( *(_DWORD *)v55 != 1768169504 )
            {
              v55 += 16;
              if ( v55 == v56 )
                goto LABEL_127;
            }
            if ( v55 == v56 )
              v57 = nullptr;
            else
              v57 = *(__int64 **)(v55 + 8);
          }
LABEL_127:
          if ( v57 != nullptr )
            v2 = v57;
          v75 = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v2 + 80LL))(*v2, v2);
          return sub_14119D9E0(v54, v75, v59);
        case 2u:
          v39 = *v8;
          v40 = v8[1];
          v41 = nullptr;
          if ( *v8 != v40 )
          {
            while ( *(_DWORD *)v39 != 1869379180 )
            {
              v39 += 16;
              if ( v39 == v40 )
                goto LABEL_95;
            }
            if ( v39 == v40 )
              v41 = nullptr;
            else
              v41 = *(__int64 **)(v39 + 8);
          }
LABEL_95:
          if ( v41 != nullptr )
            v2 = v41;
          v60 = (_QWORD **)(a1 + 1);
          v61 = sub_140EAAE10(v60, v2);
          if ( v61 < 0 )
            goto LABEL_105;
          v62 = *(_QWORD *)(**v60 + 8LL * (unsigned int)v61);
          if ( v62 == 0 )
            goto LABEL_105;
          v63 = qword_141B601A0;
          v64 = *(_QWORD **)(qword_141B601A0 + 128);
          if ( *(_QWORD *)(*v64 + 8LL * *(int *)(v62 + 8)) != 0 )
            sub_140FAC350();
          sub_141758A00();
          v64[1] -= 8LL;
          v65 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v63 + 48LL))(v63);
          LOBYTE(v2) = 1;
          if ( v65 != 0 )
          {
            v66 = v65;
            for ( i = 0; i != v66; ++i )
              *(_DWORD *)((*(__int64 (__fastcall **)(__int64, _QWORD))(*(_QWORD *)v63 + 16LL))(v63, (unsigned int)i) + 8) = i;
          }
          return (unsigned int)v2;
        case 3u:
          LOBYTE(v2) = 1;
          v42 = *(_QWORD *)(a1[1] + 8) - *(_QWORD *)a1[1];
          if ( v42 != 0 )
          {
            v43 = v42 >> 3;
            do
            {
              v44 = *(_QWORD *)(*(_QWORD *)a1[1] + 8 * v43-- - 8);
              if ( v44 != 0 )
              {
                v45 = qword_141B601A0;
                v46 = *(_QWORD **)(qword_141B601A0 + 128);
                if ( *(_QWORD *)(*v46 + 8LL * *(int *)(v44 + 8)) != 0 )
                  sub_140FAC350();
                sub_141758A00();
                v46[1] -= 8LL;
                v47 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v45 + 48LL))(v45);
                if ( v47 != 0 )
                {
                  v48 = v47;
                  for ( j = 0; j != v48; ++j )
                    *(_DWORD *)((*(__int64 (__fastcall **)(__int64, _QWORD))(*(_QWORD *)v45 + 16LL))(
                                  v45,
                                  (unsigned int)j)
                              + 8) = j;
                }
              }
            }
            while ( v43 != 0 );
          }
          return (unsigned int)v2;
        case 4u:
          v50 = *v8;
          v51 = v8[1];
          v52 = nullptr;
          if ( v50 == v51 )
            goto LABEL_108;
          break;
        case 5u:
          sub_140DF3CB0(0);
          LOBYTE(v2) = 1;
          return (unsigned int)v2;
        default:
          goto LABEL_105;
      }
      while ( *(_DWORD *)v50 != 1869379180 )
      {
        v50 += 16;
        if ( v50 == v51 )
          goto LABEL_108;
      }
      if ( v50 == v51 )
        v52 = nullptr;
      else
        v52 = *(__int64 **)(v50 + 8);
LABEL_108:
      v69 = sub_14152B6C0(*a1);
      if ( v69 != 0 )
      {
        if ( v52 == nullptr )
          v52 = &qword_141B5A4A0;
        v70 = (_QWORD *)(*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(*(_QWORD *)*v52 + 176LL))(*v52, v52, 0);
        v71 = v70[1] - *v70;
        if ( v71 != 0 )
        {
          v72 = v71 >> 4;
          v73 = 8;
          do
          {
            v74 = *(__int64 **)(*v70 + v73);
            if ( v74 == nullptr )
              v74 = &qword_141B5A4A0;
            sub_14119D9E0(v69, *(unsigned int *)(*v70 + v73 - 8), v74);
            v73 += 16;
            --v72;
          }
          while ( v72 != 0 );
        }
      }
      LOBYTE(v2) = v69 != 0;
      return (unsigned int)v2;
    }
LABEL_105:
    LODWORD(v2) = 0;
    return (unsigned int)v2;
  }
  if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(v7 + 8))(v6, a2) != 11 )
    goto LABEL_105;
  v76 = (_QWORD *)(*(__int64 (__fastcall **)(__int64 *, __int64 **, _QWORD))(**a2 + 184))(*a2, a2, 0);
  v12 = *(_QWORD *)(a1[1] + 8) - *(_QWORD *)a1[1];
  if ( v12 != 0 )
  {
    v13 = v12 >> 3;
    do
    {
      v14 = *(_QWORD *)(*(_QWORD *)a1[1] + 8 * v13-- - 8);
      if ( v14 != 0 )
      {
        v15 = qword_141B601A0;
        v16 = *(_QWORD **)(qword_141B601A0 + 128);
        if ( *(_QWORD *)(*v16 + 8LL * *(int *)(v14 + 8)) != 0 )
          sub_140FAC350();
        sub_141758A00();
        v16[1] -= 8LL;
        v17 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v15 + 48LL))(v15);
        if ( v17 != 0 )
        {
          v18 = v17;
          for ( k = 0; k != v18; ++k )
            *(_DWORD *)((*(__int64 (__fastcall **)(__int64, _QWORD))(*(_QWORD *)v15 + 16LL))(v15, (unsigned int)k) + 8) = k;
        }
      }
    }
    while ( v13 != 0 );
  }
  v20 = v76[1] - *v76;
  if ( v20 != 0 )
  {
    v21 = v20 >> 3;
    v22 = 1;
    if ( v21 >= 2 )
      v22 = v21;
    for ( m = 0; m != v22; ++m )
    {
      v24 = *(__int64 **)(*v76 + 8 * m);
      v2 = a1;
      v25 = sub_14152B6C0(*a1);
      if ( v25 != 0 )
      {
        v26 = v25;
        if ( v24 == nullptr )
          v24 = &qword_141B5A4A0;
        v27 = (_QWORD *)(*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(*(_QWORD *)*v24 + 176LL))(*v24, v24, 0);
        v28 = v27[1] - *v27;
        if ( v28 != 0 )
        {
          v29 = v28 >> 4;
          v30 = 8;
          do
          {
            v31 = *(__int64 **)(*v27 + v30);
            if ( v31 == nullptr )
              v31 = &qword_141B5A4A0;
            sub_14119D9E0(v26, *(unsigned int *)(*v27 + v30 - 8), v31);
            v30 += 16;
            --v29;
          }
          while ( v29 != 0 );
        }
      }
      a1 = v2;
    }
  }
  v32 = qword_141B60C38;
  v33 = qword_141B60C30;
  if ( qword_141B60C30 == qword_141B60C38 )
    goto LABEL_35;
  while ( *(_DWORD *)v33 != 1986359923 )
  {
    v33 += 16;
    if ( v33 == qword_141B60C38 )
      goto LABEL_35;
  }
  if ( v33 == qword_141B60C38 || (LOBYTE(v2) = 1, *(_QWORD *)(v33 + 8) == 0) )
  {
LABEL_35:
    LOBYTE(v2) = 1;
    LOBYTE(v32) = 1;
    sub_140DF3CB0(v32);
  }
  return (unsigned int)v2;
}
