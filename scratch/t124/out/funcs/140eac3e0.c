__int64 __fastcall sub_140EAC3E0(__int64 **a1, __int64 **a2)
{
  __int64 *i; // rdi
  char v5; // al
  __int64 *v6; // rcx
  __int64 v7; // rsi
  __int64 *v8; // rbx
  __int64 v9; // rax
  __int64 v10; // rcx
  __int64 v11; // rdx
  __int64 *v12; // rdx
  _QWORD *v13; // r15
  __int64 v14; // rax
  __int64 v15; // rax
  __int64 v16; // rcx
  __int64 v17; // rcx
  __int64 v18; // rcx
  __int64 v19; // rbx
  __int64 *v20; // rsi
  unsigned __int64 v21; // rcx
  __int64 *v22; // rsi
  __int64 v23; // rax
  unsigned __int64 v24; // rax
  __int64 v25; // rsi
  __int64 *v26; // rdx
  __int64 v27; // rax
  __int64 *v28; // rdx
  unsigned __int8 *v29; // rsi
  _QWORD **v30; // r14
  __int64 v31; // rax
  __int64 v32; // rcx
  __int64 *v33; // rdx
  __int64 v34; // rcx
  __int64 v35; // rdx
  __int64 *v36; // rax
  __int64 v37; // rax
  __int64 v38; // rax
  __int64 v39; // rcx
  __int64 v40; // rcx
  __int64 v41; // rcx
  __int64 *v42; // rdx
  __int64 v43; // r9
  __int64 v44; // rbx
  __int64 v45; // rsi
  unsigned __int64 v46; // rcx
  __int64 *v47; // rbx
  __int64 v48; // rcx
  __int64 v49; // rdx
  __int64 *v50; // rax
  int v51; // eax
  __int64 v52; // r14
  __int64 v53; // rsi
  __int64 v54; // rcx
  __int64 *v55; // rdx
  __int64 v56; // rax
  __int64 *v57; // rbx
  int v58; // eax
  __int64 *v59; // rax
  __int64 v60; // r8
  __int64 v61; // rbx
  __int64 v62; // rcx
  __int64 v63; // rsi
  __int64 *v64; // rbx
  __int64 v66; // rdx
  __int64 v67; // rdx
  __int64 v68; // rax
  unsigned int v69; // eax
  __int64 v70; // [rsp+20h] [rbp-38h] BYREF
  unsigned __int64 v71; // [rsp+28h] [rbp-30h]

  v5 = (*(__int64 (__fastcall **)(__int64 *))(**a2 + 8))(a1: *a2);
  v6 = *a2;
  v7 = **a2;
  if ( v5 != 10 )
  {
    if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(v7 + 8))(a1: v6, a2) == 11 )
    {
      v13 = (_QWORD *)(*(__int64 (__fastcall **)(__int64 *, __int64 **, _QWORD))(**a2 + 184))(a1: *a2, a2, a3: 0);
      v14 = a1[1][1] - *a1[1];
      if ( v14 != 0 )
      {
        v15 = v14 >> 3;
        do
        {
          v12 = *(__int64 **)(*a1[1] + 8 * v15-- - 8);
          if ( v12 != nullptr )
          {
            v19 = **a1;
            v20 = *(__int64 **)(v19 + 72);
            i = *(__int64 **)(v19 + 80);
            if ( i != v20 )
            {
              v21 = ((char *)i - (char *)v20) >> 4;
              if ( v21 < 2 )
                v21 = 1;
              v22 = v20 - 2;
              while ( 1 )
              {
                v22 += 2;
                if ( v22 == v12 )
                  break;
                if ( --v21 == 0 )
                  goto LABEL_11;
              }
              v16 = *v12;
              v71 = v12[1];
              v70 = v16;
              v17 = *(i - 2);
              v12[1] = *(i - 1);
              *v12 = v17;
              v18 = v70;
              v12 = (__int64 *)v71;
              *(i - 1) = v71;
              *(i - 2) = v18;
              *(_QWORD *)(v19 + 80) -= 16LL;
            }
          }
LABEL_11:
          ;
        }
        while ( v15 != 0 );
      }
      v23 = v13[1] - *v13;
      if ( v23 != 0 )
      {
        v24 = v23 >> 3;
        v25 = 1;
        if ( v24 >= 2 )
          v25 = v24;
        for ( i = nullptr; i != (__int64 *)v25; i = (__int64 *)((char *)i + 1) )
        {
          v26 = *(__int64 **)(*v13 + 8LL * (_QWORD)i);
          if ( v26 == nullptr )
            v26 = &qword_141B5A4A0;
          sub_140EACC60(a1, a2: v26);
        }
      }
      v27 = qword_141B60C30;
      if ( qword_141B60C30 == qword_141B60C38 )
        goto LABEL_30;
      while ( *(_DWORD *)v27 != 1986359923 )
      {
        v27 += 16;
        if ( v27 == qword_141B60C38 )
          goto LABEL_30;
      }
      if ( v27 == qword_141B60C38 || (LOBYTE(i) = 1, *(_QWORD *)(v27 + 8) == 0) )
      {
LABEL_30:
        LOBYTE(i) = 1;
        LOBYTE(v12) = 1;
        sub_140EAC9F0(a1, a2: v12);
      }
      return (unsigned int)i;
    }
    goto LABEL_106;
  }
  LODWORD(i) = 0;
  v8 = (__int64 *)(*(__int64 (__fastcall **)(__int64 *, __int64 **, _QWORD))(v7 + 176))(a1: v6, a2, a3: 0);
  v9 = *v8;
  v10 = v8[1];
  if ( *v8 == v10 )
    return (unsigned int)i;
  v11 = *v8;
  while ( *(_DWORD *)v11 != 1819504496 )
  {
    v11 += 16;
    if ( v11 == v10 )
      goto LABEL_106;
  }
  if ( v11 == v10 || *(_QWORD *)(v11 + 8) == 0 )
  {
LABEL_106:
    LODWORD(i) = 0;
    return (unsigned int)i;
  }
  v28 = nullptr;
  while ( *(_DWORD *)v9 != 1819504496 )
  {
    v9 += 16;
    if ( v9 == v10 )
      goto LABEL_43;
  }
  if ( v9 == v10 )
    v28 = nullptr;
  else
    v28 = *(__int64 **)(v9 + 8);
LABEL_43:
  i = &qword_141B5A4A0;
  if ( v28 == nullptr )
    v28 = &qword_141B5A4A0;
  switch ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)*v28 + 64LL))(a1: *v28) )
  {
    case 0u:
      v29 = (unsigned __int8 *)*a1;
      v70 = 0;
      v71 = 0xFF00FF00FF000000uLL;
      if ( *(_QWORD *)(*(_QWORD *)v29 + 80LL) - *(_QWORD *)(*(_QWORD *)v29 + 72LL) > 0x7CFu
        || (unsigned __int8)sub_141106030(a1: &v70, a2: v29[40]) == 0
        || *(_QWORD *)(*(_QWORD *)v29 + 80LL) - *(_QWORD *)(*(_QWORD *)v29 + 72LL) > 0xFEFu )
      {
        goto LABEL_106;
      }
      sub_140E02B10(a1: *(_QWORD *)v29 + 72LL, a2: &v70);
      LOBYTE(i) = 1;
      return (unsigned int)i;
    case 1u:
      v30 = a1 + 1;
      v31 = *v8;
      v32 = v8[1];
      v33 = nullptr;
      if ( *v8 != v32 )
      {
        while ( *(_DWORD *)v31 != 1869379180 )
        {
          v31 += 16;
          if ( v31 == v32 )
            goto LABEL_82;
        }
        if ( v31 == v32 )
          v33 = nullptr;
        else
          v33 = *(__int64 **)(v31 + 8);
      }
LABEL_82:
      if ( v33 == nullptr )
        v33 = &qword_141B5A4A0;
      v51 = sub_140DF48E0(a1: v30, a2: v33);
      if ( v51 < 0 )
        goto LABEL_106;
      v52 = *(_QWORD *)(**v30 + 8LL * (unsigned int)v51);
      if ( v52 == 0 )
        goto LABEL_106;
      v53 = *v8;
      v54 = v8[1];
      v55 = nullptr;
      if ( *v8 == v54 )
      {
        v57 = &qword_141B5A4A0;
      }
      else
      {
        v56 = *v8;
        while ( *(_DWORD *)v56 != 1986096245 )
        {
          v56 += 16;
          if ( v56 == v54 )
            goto LABEL_114;
        }
        if ( v56 == v54 )
          v55 = nullptr;
        else
          v55 = *(__int64 **)(v56 + 8);
LABEL_114:
        v57 = &qword_141B5A4A0;
        if ( v55 != nullptr )
          v57 = v55;
        v55 = nullptr;
        while ( *(_DWORD *)v53 != 1768169504 )
        {
          v53 += 16;
          if ( v53 == v54 )
            goto LABEL_123;
        }
        if ( v53 == v54 )
          v55 = nullptr;
        else
          v55 = *(__int64 **)(v53 + 8);
      }
LABEL_123:
      if ( v55 != nullptr )
        i = v55;
      v69 = (*(__int64 (__fastcall **)(_QWORD, __int64 *))(*(_QWORD *)*i + 80LL))(a1: *i, a2: i);
      return sub_141107F10(a1: v52, a2: v69, a3: v57);
    case 2u:
      v34 = *v8;
      v35 = v8[1];
      v36 = nullptr;
      if ( *v8 != v35 )
      {
        while ( *(_DWORD *)v34 != 1869379180 )
        {
          v34 += 16;
          if ( v34 == v35 )
            goto LABEL_95;
        }
        if ( v34 == v35 )
          v36 = nullptr;
        else
          v36 = *(__int64 **)(v34 + 8);
      }
LABEL_95:
      if ( v36 != nullptr )
        i = v36;
      v58 = sub_140DF48E0(a1: a1 + 1, a2: i);
      if ( v58 < 0 )
        goto LABEL_106;
      v59 = *(__int64 **)(*a1[1] + 8LL * (unsigned int)v58);
      if ( v59 == nullptr )
        goto LABEL_106;
      v60 = **a1;
      v61 = *(_QWORD *)(v60 + 72);
      v62 = *(_QWORD *)(v60 + 80);
      LOBYTE(i) = 1;
      if ( v62 != v61 )
      {
        v63 = 1;
        if ( (unsigned __int64)((v62 - v61) >> 4) >= 2 )
          v63 = (v62 - v61) >> 4;
        v64 = (__int64 *)(v61 - 16);
        while ( 1 )
        {
          v64 += 2;
          if ( v64 == v59 )
            break;
          if ( --v63 == 0 )
            return (unsigned int)i;
        }
        v66 = *v59;
        v71 = v59[1];
        v70 = v66;
        v67 = *(_QWORD *)(v62 - 16);
        v59[1] = *(_QWORD *)(v62 - 8);
        *v59 = v67;
        v68 = v70;
        *(_QWORD *)(v62 - 8) = v71;
        *(_QWORD *)(v62 - 16) = v68;
        *(_QWORD *)(v60 + 80) -= 16LL;
      }
      return (unsigned int)i;
    case 3u:
      LOBYTE(i) = 1;
      v37 = a1[1][1] - *a1[1];
      if ( v37 == 0 )
        return (unsigned int)i;
      v38 = v37 >> 3;
      do
      {
        v42 = *(__int64 **)(*a1[1] + 8 * v38-- - 8);
        if ( v42 != nullptr )
        {
          v43 = **a1;
          v44 = *(_QWORD *)(v43 + 72);
          v45 = *(_QWORD *)(v43 + 80);
          if ( v45 != v44 )
          {
            v46 = (v45 - v44) >> 4;
            if ( v46 < 2 )
              v46 = 1;
            v47 = (__int64 *)(v44 - 16);
            while ( 1 )
            {
              v47 += 2;
              if ( v47 == v42 )
                break;
              if ( --v46 == 0 )
                goto LABEL_61;
            }
            v39 = *v42;
            v71 = v42[1];
            v70 = v39;
            v40 = *(_QWORD *)(v45 - 16);
            v42[1] = *(_QWORD *)(v45 - 8);
            *v42 = v40;
            v41 = v70;
            *(_QWORD *)(v45 - 8) = v71;
            *(_QWORD *)(v45 - 16) = v41;
            *(_QWORD *)(v43 + 80) -= 16LL;
          }
        }
LABEL_61:
        ;
      }
      while ( v38 != 0 );
      return (unsigned int)i;
    case 4u:
      v48 = *v8;
      v49 = v8[1];
      v50 = nullptr;
      if ( *v8 == v49 )
        goto LABEL_110;
      break;
    case 5u:
      sub_140EAC9F0(a1, a2: 0);
      LOBYTE(i) = 1;
      return (unsigned int)i;
    default:
      goto LABEL_106;
  }
  while ( *(_DWORD *)v48 != 1869379180 )
  {
    v48 += 16;
    if ( v48 == v49 )
      goto LABEL_110;
  }
  if ( v48 == v49 )
    v50 = nullptr;
  else
    v50 = *(__int64 **)(v48 + 8);
LABEL_110:
  if ( v50 != nullptr )
    i = v50;
  return sub_140EACC60(a1, a2: i);
}
