__int64 __fastcall sub_141051740(_QWORD *a1, __int64 **a2)
{
  __int64 i; // rdi
  char v5; // al
  __int64 *v6; // rcx
  __int64 v7; // rbp
  __int64 *v8; // rsi
  __int64 v9; // rax
  __int64 v10; // rcx
  __int64 v11; // rdx
  _QWORD *v12; // rax
  __int64 v13; // rsi
  __int64 v14; // rsi
  bool v15; // zf
  __int64 v16; // rax
  unsigned __int64 v17; // rax
  __int64 v18; // r12
  __int64 *v19; // rsi
  _QWORD *v20; // r15
  __int64 v21; // rax
  __int64 v22; // rbx
  _QWORD *v23; // rsi
  __int64 v24; // rbp
  __int64 v25; // rbp
  __int64 v26; // r14
  __int64 *v27; // r8
  __int64 v28; // rax
  __int64 *v29; // rdx
  __int64 *v30; // r15
  _QWORD *v31; // rbx
  __int64 v32; // rax
  __int64 v33; // rcx
  __int64 *v34; // rdx
  __int64 v35; // rcx
  __int64 v36; // rdx
  __int64 *v37; // rax
  _QWORD *v38; // rax
  __int64 v39; // rsi
  __int64 v40; // rsi
  __int64 v41; // rax
  __int64 v42; // rcx
  int v43; // eax
  __int64 v44; // rdi
  __int64 v45; // rbp
  __int64 v46; // rcx
  __int64 *v47; // rdx
  __int64 v48; // rax
  __int64 *v49; // rbx
  int v50; // eax
  __int64 v52; // rsi
  _QWORD *v53; // rbx
  __int64 v54; // rbp
  __int64 *v55; // r8
  unsigned int v56; // eax
  _QWORD *v57; // [rsp+20h] [rbp-48h]

  v5 = (*(__int64 (__fastcall **)(__int64 *))(**a2 + 8))(*a2);
  v6 = *a2;
  v7 = **a2;
  if ( v5 == 10 )
  {
    LODWORD(i) = 0;
    v8 = (__int64 *)(*(__int64 (__fastcall **)(__int64 *, __int64 **, _QWORD))(v7 + 176))(v6, a2, 0);
    v9 = *v8;
    v10 = v8[1];
    if ( *v8 == v10 )
      return (unsigned int)i;
    v11 = *v8;
    while ( *(_DWORD *)v11 != 1819504496 )
    {
      v11 += 16;
      if ( v11 == v10 )
        goto LABEL_90;
    }
    if ( v11 != v10 && *(_QWORD *)(v11 + 8) != 0 )
    {
      v29 = nullptr;
      while ( *(_DWORD *)v9 != 1819504496 )
      {
        v9 += 16;
        if ( v9 == v10 )
          goto LABEL_43;
      }
      if ( v9 == v10 )
        v29 = nullptr;
      else
        v29 = *(__int64 **)(v9 + 8);
LABEL_43:
      v30 = &qword_141B5A4A0;
      if ( v29 == nullptr )
        v29 = &qword_141B5A4A0;
      switch ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)*v29 + 64LL))(*v29) )
      {
        case 0u:
          LOBYTE(i) = sub_1415D11B0(*a1) != 0;
          return (unsigned int)i;
        case 1u:
          v31 = a1 + 1;
          v32 = *v8;
          v33 = v8[1];
          v34 = nullptr;
          if ( *v8 != v33 )
          {
            while ( *(_DWORD *)v32 != 1869379180 )
            {
              v32 += 16;
              if ( v32 == v33 )
                goto LABEL_72;
            }
            if ( v32 == v33 )
              v34 = nullptr;
            else
              v34 = *(__int64 **)(v32 + 8);
          }
LABEL_72:
          if ( v34 == nullptr )
            v34 = &qword_141B5A4A0;
          v43 = sub_141051CC0(v31, v34);
          if ( v43 < 0 )
            goto LABEL_90;
          v44 = *(_QWORD *)(**(_QWORD **)(*(_QWORD *)*v31 + 368LL) + 8LL * (unsigned int)v43);
          if ( v44 == 0 )
            goto LABEL_90;
          v45 = *v8;
          v46 = v8[1];
          v47 = nullptr;
          if ( *v8 == v46 )
          {
            v49 = &qword_141B5A4A0;
          }
          else
          {
            v48 = *v8;
            while ( *(_DWORD *)v48 != 1986096245 )
            {
              v48 += 16;
              if ( v48 == v46 )
                goto LABEL_103;
            }
            if ( v48 == v46 )
              v47 = nullptr;
            else
              v47 = *(__int64 **)(v48 + 8);
LABEL_103:
            v49 = &qword_141B5A4A0;
            if ( v47 != nullptr )
              v49 = v47;
            v47 = nullptr;
            while ( *(_DWORD *)v45 != 1768169504 )
            {
              v45 += 16;
              if ( v45 == v46 )
                goto LABEL_112;
            }
            if ( v45 == v46 )
              v47 = nullptr;
            else
              v47 = *(__int64 **)(v45 + 8);
          }
LABEL_112:
          if ( v47 != nullptr )
            v30 = v47;
          v56 = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v30 + 80LL))(*v30, v30);
          return sub_141073780(v44, v56, v49);
        case 2u:
          v35 = *v8;
          v36 = v8[1];
          v37 = nullptr;
          if ( *v8 != v36 )
          {
            while ( *(_DWORD *)v35 != 1869379180 )
            {
              v35 += 16;
              if ( v35 == v36 )
                goto LABEL_85;
            }
            if ( v35 == v36 )
              v37 = nullptr;
            else
              v37 = *(__int64 **)(v35 + 8);
          }
LABEL_85:
          if ( v37 != nullptr )
            v30 = v37;
          v50 = sub_141051CC0(a1 + 1, v30);
          if ( v50 < 0 || *(_QWORD *)(**(_QWORD **)(*(_QWORD *)a1[1] + 368LL) + 8LL * (unsigned int)v50) == 0 )
            goto LABEL_90;
          sub_14104C270(
            *(_QWORD *)(*(_QWORD *)*a1 + 368LL),
            *(_QWORD *)(**(_QWORD **)(*(_QWORD *)*a1 + 368LL) + 8LL * (unsigned int)v50));
          LOBYTE(i) = 1;
          return (unsigned int)i;
        case 3u:
          v38 = *(_QWORD **)(*(_QWORD *)a1[1] + 368LL);
          LOBYTE(i) = 1;
          v39 = v38[1] - *v38;
          if ( v39 != 0 )
          {
            v40 = v39 >> 3;
            do
            {
              v15 = *(_QWORD *)(**(_QWORD **)(*(_QWORD *)a1[1] + 368LL) + 8 * v40-- - 8) == 0;
              if ( !v15 )
                sub_14104C270(
                  *(_QWORD *)(*(_QWORD *)*a1 + 368LL),
                  *(_QWORD *)(**(_QWORD **)(*(_QWORD *)*a1 + 368LL) + 8 * v40));
            }
            while ( v40 != 0 );
          }
          return (unsigned int)i;
        case 4u:
          v41 = *v8;
          v42 = v8[1];
          i = 0;
          if ( *v8 == v42 )
            goto LABEL_93;
          break;
        case 5u:
          sub_140DD5C90();
          LOBYTE(i) = 1;
          return (unsigned int)i;
        default:
          goto LABEL_90;
      }
      while ( *(_DWORD *)v41 != 1869379180 )
      {
        v41 += 16;
        if ( v41 == v42 )
          goto LABEL_93;
      }
      if ( v41 == v42 )
        i = 0;
      else
        i = *(_QWORD *)(v41 + 8);
LABEL_93:
      v52 = sub_1415D11B0(*a1);
      if ( v52 != 0 )
      {
        if ( i == 0 )
          i = (__int64)&qword_141B5A4A0;
        v53 = (_QWORD *)(*(__int64 (__fastcall **)(_QWORD, __int64, _QWORD))(**(_QWORD **)i + 176LL))(
                          *(_QWORD *)i,
                          i,
                          0);
        i = v53[1] - *v53;
        if ( i != 0 )
        {
          i >>= 4;
          v54 = 8;
          do
          {
            v55 = *(__int64 **)(*v53 + v54);
            if ( v55 == nullptr )
              v55 = &qword_141B5A4A0;
            sub_141073780(v52, *(unsigned int *)(*v53 + v54 - 8), v55);
            v54 += 16;
            --i;
          }
          while ( i != 0 );
        }
      }
      LOBYTE(i) = v52 != 0;
      return (unsigned int)i;
    }
LABEL_90:
    LODWORD(i) = 0;
    return (unsigned int)i;
  }
  if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(v7 + 8))(v6, a2) != 11 )
    goto LABEL_90;
  v57 = (_QWORD *)(*(__int64 (__fastcall **)(__int64 *, __int64 **, _QWORD))(**a2 + 184))(*a2, a2, 0);
  v12 = *(_QWORD **)(*(_QWORD *)a1[1] + 368LL);
  v13 = v12[1] - *v12;
  if ( v13 != 0 )
  {
    v14 = v13 >> 3;
    do
    {
      v15 = *(_QWORD *)(**(_QWORD **)(*(_QWORD *)a1[1] + 368LL) + 8 * v14-- - 8) == 0;
      if ( !v15 )
        sub_14104C270(*(_QWORD *)(*(_QWORD *)*a1 + 368LL), *(_QWORD *)(**(_QWORD **)(*(_QWORD *)*a1 + 368LL) + 8 * v14));
    }
    while ( v14 != 0 );
  }
  v16 = v57[1] - *v57;
  if ( v16 != 0 )
  {
    v17 = v16 >> 3;
    v18 = 1;
    if ( v17 >= 2 )
      v18 = v17;
    for ( i = 0; i != v18; ++i )
    {
      v19 = *(__int64 **)(*v57 + 8 * i);
      v20 = a1;
      v21 = sub_1415D11B0(*a1);
      if ( v21 != 0 )
      {
        v22 = v21;
        if ( v19 == nullptr )
          v19 = &qword_141B5A4A0;
        v23 = (_QWORD *)(*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(*(_QWORD *)*v19 + 176LL))(*v19, v19, 0);
        v24 = v23[1] - *v23;
        if ( v24 != 0 )
        {
          v25 = v24 >> 4;
          v26 = 8;
          do
          {
            v27 = *(__int64 **)(*v23 + v26);
            if ( v27 == nullptr )
              v27 = &qword_141B5A4A0;
            sub_141073780(v22, *(unsigned int *)(*v23 + v26 - 8), v27);
            v26 += 16;
            --v25;
          }
          while ( v25 != 0 );
        }
      }
      a1 = v20;
    }
  }
  v28 = qword_141B60C30;
  if ( qword_141B60C30 == qword_141B60C38 )
    goto LABEL_30;
  while ( *(_DWORD *)v28 != 1986359923 )
  {
    v28 += 16;
    if ( v28 == qword_141B60C38 )
      goto LABEL_30;
  }
  if ( v28 == qword_141B60C38 || (LOBYTE(i) = 1, *(_QWORD *)(v28 + 8) == 0) )
  {
LABEL_30:
    LOBYTE(i) = 1;
    sub_140DD5C90();
  }
  return (unsigned int)i;
}
