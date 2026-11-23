__int64 __fastcall sub_140EADC50(__int64 *a1, __int64 **a2)
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
  _QWORD *v16; // rdi
  __int64 v17; // rsi
  __int64 v18; // rcx
  __int64 v19; // rax
  __int64 v20; // rsi
  __int64 k; // rdi
  __int64 v22; // rax
  unsigned __int64 v23; // rax
  __int64 v24; // r12
  __int64 m; // rdi
  __int64 *v26; // rsi
  __int64 v27; // rax
  __int64 v28; // rbx
  _QWORD *v29; // rsi
  __int64 v30; // rbp
  __int64 v31; // rbp
  __int64 v32; // r14
  __int64 *v33; // r8
  __int64 v34; // rcx
  __int64 v35; // rax
  __int64 *v36; // rdx
  _QWORD **v37; // r14
  __int64 v38; // rax
  __int64 v39; // rcx
  __int64 *v40; // rdx
  __int64 v41; // rcx
  __int64 v42; // rdx
  __int64 *v43; // rax
  __int64 v44; // r12
  __int64 v45; // r12
  __int64 v46; // rax
  __int64 v47; // rbx
  _QWORD *v48; // rdi
  __int64 v49; // rsi
  __int64 v50; // rcx
  __int64 v51; // rax
  __int64 v52; // rsi
  __int64 j; // rdi
  __int64 v54; // rax
  __int64 v55; // rcx
  __int64 *v56; // rbx
  int v57; // eax
  __int64 v58; // rsi
  __int64 v59; // rbp
  __int64 v60; // rcx
  __int64 *v61; // rdx
  __int64 v62; // rax
  __int64 *v63; // rbx
  _QWORD **v64; // r14
  int v65; // eax
  __int64 v66; // rax
  __int64 v67; // rsi
  _QWORD *v68; // rdi
  __int64 v69; // rbx
  __int64 v70; // rcx
  __int64 v71; // rax
  __int64 v72; // r14
  __int64 i; // rbx
  __int64 v75; // rsi
  _QWORD *v76; // rbx
  __int64 v77; // rdi
  __int64 v78; // rdi
  __int64 v79; // rbp
  __int64 *v80; // r8
  unsigned int v81; // eax
  _QWORD *v82; // [rsp+20h] [rbp-48h]

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
        goto LABEL_114;
    }
    if ( v11 != v10 && *(_QWORD *)(v11 + 8) != 0 )
    {
      v36 = nullptr;
      while ( *(_DWORD *)v9 != 1819504496 )
      {
        v9 += 16;
        if ( v9 == v10 )
          goto LABEL_51;
      }
      if ( v9 == v10 )
        v36 = nullptr;
      else
        v36 = *(__int64 **)(v9 + 8);
LABEL_51:
      v2 = &qword_141B5A4A0;
      if ( v36 == nullptr )
        v36 = &qword_141B5A4A0;
      switch ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)*v36 + 64LL))(*v36) )
      {
        case 0u:
          LOBYTE(v2) = sub_141532780(*a1) != 0;
          return (unsigned int)v2;
        case 1u:
          v37 = (_QWORD **)(a1 + 1);
          v38 = *v8;
          v39 = v8[1];
          v40 = nullptr;
          if ( *v8 != v39 )
          {
            while ( *(_DWORD *)v38 != 1869379180 )
            {
              v38 += 16;
              if ( v38 == v39 )
                goto LABEL_88;
            }
            if ( v38 == v39 )
              v40 = nullptr;
            else
              v40 = *(__int64 **)(v38 + 8);
          }
LABEL_88:
          if ( v40 == nullptr )
            v40 = &qword_141B5A4A0;
          v57 = sub_140EAE300(v37, v40);
          if ( v57 < 0 )
            goto LABEL_114;
          v58 = *(_QWORD *)(**v37 + 8LL * (unsigned int)v57);
          if ( v58 == 0 )
            goto LABEL_114;
          v59 = *v8;
          v60 = v8[1];
          v61 = nullptr;
          if ( *v8 == v60 )
          {
            v63 = &qword_141B5A4A0;
          }
          else
          {
            v62 = *v8;
            while ( *(_DWORD *)v62 != 1986096245 )
            {
              v62 += 16;
              if ( v62 == v60 )
                goto LABEL_127;
            }
            if ( v62 == v60 )
              v61 = nullptr;
            else
              v61 = *(__int64 **)(v62 + 8);
LABEL_127:
            v63 = &qword_141B5A4A0;
            if ( v61 != nullptr )
              v63 = v61;
            v61 = nullptr;
            while ( *(_DWORD *)v59 != 1768169504 )
            {
              v59 += 16;
              if ( v59 == v60 )
                goto LABEL_136;
            }
            if ( v59 == v60 )
              v61 = nullptr;
            else
              v61 = *(__int64 **)(v59 + 8);
          }
LABEL_136:
          if ( v61 != nullptr )
            v2 = v61;
          v81 = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v2 + 80LL))(*v2, v2);
          return sub_141545680(v58, v81, v63);
        case 2u:
          v41 = *v8;
          v42 = v8[1];
          v43 = nullptr;
          if ( *v8 != v42 )
          {
            while ( *(_DWORD *)v41 != 1869379180 )
            {
              v41 += 16;
              if ( v41 == v42 )
                goto LABEL_101;
            }
            if ( v41 == v42 )
              v43 = nullptr;
            else
              v43 = *(__int64 **)(v41 + 8);
          }
LABEL_101:
          if ( v43 != nullptr )
            v2 = v43;
          v64 = (_QWORD **)(a1 + 1);
          v65 = sub_140EAE300(v64, v2);
          if ( v65 < 0 )
            goto LABEL_114;
          v66 = *(_QWORD *)(**v64 + 8LL * (unsigned int)v65);
          if ( v66 == 0 )
            goto LABEL_114;
          v67 = qword_141B60190;
          v68 = *(_QWORD **)(qword_141B60190 + 128);
          v69 = *(_QWORD *)(*v68 + 8LL * *(int *)(v66 + 8));
          if ( v69 != 0 )
          {
            v70 = *(_QWORD *)(v69 + 56);
            if ( v70 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v70 - 4)) == 0 )
              sub_1412EC9A0(v70 - 4);
            sub_140ED1840(v69);
          }
          sub_141758A00();
          v68[1] -= 8LL;
          v71 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v67 + 48LL))(v67);
          LOBYTE(v2) = 1;
          if ( v71 != 0 )
          {
            v72 = v71;
            for ( i = 0; i != v72; ++i )
              *(_DWORD *)((*(__int64 (__fastcall **)(__int64, _QWORD))(*(_QWORD *)v67 + 16LL))(v67, (unsigned int)i) + 8) = i;
          }
          return (unsigned int)v2;
        case 3u:
          LOBYTE(v2) = 1;
          v44 = *(_QWORD *)(a1[1] + 8) - *(_QWORD *)a1[1];
          if ( v44 != 0 )
          {
            v45 = v44 >> 3;
            do
            {
              v46 = *(_QWORD *)(*(_QWORD *)a1[1] + 8 * v45-- - 8);
              if ( v46 != 0 )
              {
                v47 = qword_141B60190;
                v48 = *(_QWORD **)(qword_141B60190 + 128);
                v49 = *(_QWORD *)(*v48 + 8LL * *(int *)(v46 + 8));
                if ( v49 != 0 )
                {
                  v50 = *(_QWORD *)(v49 + 56);
                  if ( v50 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v50 - 4)) == 0 )
                    sub_1412EC9A0(v50 - 4);
                  sub_140ED1840(v49);
                }
                sub_141758A00();
                v48[1] -= 8LL;
                v51 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v47 + 48LL))(v47);
                if ( v51 != 0 )
                {
                  v52 = v51;
                  for ( j = 0; j != v52; ++j )
                    *(_DWORD *)((*(__int64 (__fastcall **)(__int64, _QWORD))(*(_QWORD *)v47 + 16LL))(
                                  v47,
                                  (unsigned int)j)
                              + 8) = j;
                }
              }
            }
            while ( v45 != 0 );
          }
          return (unsigned int)v2;
        case 4u:
          v54 = *v8;
          v55 = v8[1];
          v56 = nullptr;
          if ( v54 == v55 )
            goto LABEL_117;
          break;
        case 5u:
          sub_140DF3CB0(0);
          LOBYTE(v2) = 1;
          return (unsigned int)v2;
        default:
          goto LABEL_114;
      }
      while ( *(_DWORD *)v54 != 1869379180 )
      {
        v54 += 16;
        if ( v54 == v55 )
          goto LABEL_117;
      }
      if ( v54 == v55 )
        v56 = nullptr;
      else
        v56 = *(__int64 **)(v54 + 8);
LABEL_117:
      v75 = sub_141532780(*a1);
      if ( v75 != 0 )
      {
        if ( v56 == nullptr )
          v56 = &qword_141B5A4A0;
        v76 = (_QWORD *)(*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(*(_QWORD *)*v56 + 176LL))(*v56, v56, 0);
        v77 = v76[1] - *v76;
        if ( v77 != 0 )
        {
          v78 = v77 >> 4;
          v79 = 8;
          do
          {
            v80 = *(__int64 **)(*v76 + v79);
            if ( v80 == nullptr )
              v80 = &qword_141B5A4A0;
            sub_141545680(v75, *(unsigned int *)(*v76 + v79 - 8), v80);
            v79 += 16;
            --v78;
          }
          while ( v78 != 0 );
        }
      }
      LOBYTE(v2) = v75 != 0;
      return (unsigned int)v2;
    }
LABEL_114:
    LODWORD(v2) = 0;
    return (unsigned int)v2;
  }
  if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(v7 + 8))(v6, a2) != 11 )
    goto LABEL_114;
  v82 = (_QWORD *)(*(__int64 (__fastcall **)(__int64 *, __int64 **, _QWORD))(**a2 + 184))(*a2, a2, 0);
  v12 = *(_QWORD *)(a1[1] + 8) - *(_QWORD *)a1[1];
  if ( v12 != 0 )
  {
    v13 = v12 >> 3;
    do
    {
      v14 = *(_QWORD *)(*(_QWORD *)a1[1] + 8 * v13-- - 8);
      if ( v14 != 0 )
      {
        v15 = qword_141B60190;
        v16 = *(_QWORD **)(qword_141B60190 + 128);
        v17 = *(_QWORD *)(*v16 + 8LL * *(int *)(v14 + 8));
        if ( v17 != 0 )
        {
          v18 = *(_QWORD *)(v17 + 56);
          if ( v18 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v18 - 4)) == 0 )
            sub_1412EC9A0(v18 - 4);
          sub_140ED1840(v17);
        }
        sub_141758A00();
        v16[1] -= 8LL;
        v19 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v15 + 48LL))(v15);
        if ( v19 != 0 )
        {
          v20 = v19;
          for ( k = 0; k != v20; ++k )
            *(_DWORD *)((*(__int64 (__fastcall **)(__int64, _QWORD))(*(_QWORD *)v15 + 16LL))(v15, (unsigned int)k) + 8) = k;
        }
      }
    }
    while ( v13 != 0 );
  }
  v22 = v82[1] - *v82;
  if ( v22 != 0 )
  {
    v23 = v22 >> 3;
    v24 = 1;
    if ( v23 >= 2 )
      v24 = v23;
    for ( m = 0; m != v24; ++m )
    {
      v26 = *(__int64 **)(*v82 + 8 * m);
      v2 = a1;
      v27 = sub_141532780(*a1);
      if ( v27 != 0 )
      {
        v28 = v27;
        if ( v26 == nullptr )
          v26 = &qword_141B5A4A0;
        v29 = (_QWORD *)(*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(*(_QWORD *)*v26 + 176LL))(*v26, v26, 0);
        v30 = v29[1] - *v29;
        if ( v30 != 0 )
        {
          v31 = v30 >> 4;
          v32 = 8;
          do
          {
            v33 = *(__int64 **)(*v29 + v32);
            if ( v33 == nullptr )
              v33 = &qword_141B5A4A0;
            sub_141545680(v28, *(unsigned int *)(*v29 + v32 - 8), v33);
            v32 += 16;
            --v31;
          }
          while ( v31 != 0 );
        }
      }
      a1 = v2;
    }
  }
  v34 = qword_141B60C38;
  v35 = qword_141B60C30;
  if ( qword_141B60C30 == qword_141B60C38 )
    goto LABEL_38;
  while ( *(_DWORD *)v35 != 1986359923 )
  {
    v35 += 16;
    if ( v35 == qword_141B60C38 )
      goto LABEL_38;
  }
  if ( v35 == qword_141B60C38 || (LOBYTE(v2) = 1, *(_QWORD *)(v35 + 8) == 0) )
  {
LABEL_38:
    LOBYTE(v2) = 1;
    LOBYTE(v34) = 1;
    sub_140DF3CB0(v34);
  }
  return (unsigned int)v2;
}
