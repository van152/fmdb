__int64 __fastcall sub_140ED3560(_QWORD *a1, __int64 **a2)
{
  char v4; // al
  __int64 *v5; // rcx
  __int64 v6; // rsi
  __int64 *v7; // rdi
  __int64 *v8; // rbx
  __int64 v9; // rax
  __int64 v10; // rcx
  __int64 v11; // rdx
  __int64 v12; // rbx
  __int64 v13; // rbx
  bool v14; // cf
  __int64 v15; // rdx
  __int64 v16; // rax
  unsigned __int64 v17; // rax
  __int64 v18; // rbx
  __int64 i; // rsi
  __int64 *v20; // rdx
  __int64 v21; // rcx
  __int64 v22; // rax
  __int64 *v23; // rdx
  __int64 v24; // rcx
  __int64 v25; // rdx
  __int64 *v26; // rax
  __int64 v27; // rax
  __int64 v28; // rcx
  __int64 *v29; // rdx
  __int64 v30; // rcx
  __int64 v31; // rdx
  __int64 *v32; // rax
  __int64 v33; // rbx
  __int64 v34; // rbx
  __int64 v35; // rdx
  __int64 v36; // rcx
  int v37; // eax
  __int64 v38; // rdx
  __int64 v39; // rdx
  __int64 v40; // rbx
  __int64 *v41; // rax
  int v42; // eax
  __int64 v43; // rdx

  v4 = (*(__int64 (__fastcall **)(__int64 *))(**a2 + 8))(*a2);
  v5 = *a2;
  v6 = **a2;
  if ( v4 == 10 )
  {
    LODWORD(v7) = 0;
    v8 = (__int64 *)(*(__int64 (__fastcall **)(__int64 *, __int64 **, _QWORD))(v6 + 176))(v5, a2, 0);
    v9 = *v8;
    v10 = v8[1];
    if ( *v8 == v10 )
      return (unsigned int)v7;
    v11 = *v8;
    while ( *(_DWORD *)v11 != 1819504496 )
    {
      v11 += 16;
      if ( v11 == v10 )
        goto LABEL_88;
    }
    if ( v11 != v10 && *(_QWORD *)(v11 + 8) != 0 )
    {
      v23 = nullptr;
      while ( *(_DWORD *)v9 != 1819504496 )
      {
        v9 += 16;
        if ( v9 == v10 )
          goto LABEL_36;
      }
      if ( v9 == v10 )
        v23 = nullptr;
      else
        v23 = *(__int64 **)(v9 + 8);
LABEL_36:
      v7 = &qword_141B5A4A0;
      if ( v23 == nullptr )
        v23 = &qword_141B5A4A0;
      switch ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)*v23 + 64LL))(*v23) )
      {
        case 0u:
          v24 = *v8;
          v25 = v8[1];
          v26 = nullptr;
          if ( *v8 == v25 )
            goto LABEL_68;
          while ( *(_DWORD *)v24 != 1986096245 )
          {
            v24 += 16;
            if ( v24 == v25 )
              goto LABEL_68;
          }
          goto LABEL_61;
        case 1u:
          v27 = *v8;
          v28 = v8[1];
          v29 = nullptr;
          if ( *v8 != v28 )
          {
            while ( *(_DWORD *)v27 != 1869379180 )
            {
              v27 += 16;
              if ( v27 == v28 )
                goto LABEL_73;
            }
            if ( v27 == v28 )
              v29 = nullptr;
            else
              v29 = *(__int64 **)(v27 + 8);
          }
LABEL_73:
          if ( v29 == nullptr )
            v29 = &qword_141B5A4A0;
          v37 = sub_140ED3970(a1 + 1, v29);
          if ( v37 < 0 )
            goto LABEL_88;
          v38 = *(_QWORD *)(*(_QWORD *)a1[1] + 8LL * (unsigned int)v37);
          if ( v38 == 0 || (unsigned __int8)sub_1415630D0(*a1, v38, (unsigned int)v37) == 0 )
            goto LABEL_88;
          v36 = *a1;
          v39 = *v8;
          v40 = v8[1];
          v41 = nullptr;
          if ( v39 != v40 )
          {
            while ( *(_DWORD *)v39 != 1986096245 )
            {
              v39 += 16;
              if ( v39 == v40 )
                goto LABEL_93;
            }
            if ( v39 == v40 )
              v41 = nullptr;
            else
              v41 = *(__int64 **)(v39 + 8);
          }
LABEL_93:
          if ( v41 != nullptr )
            v7 = v41;
          goto LABEL_71;
        case 2u:
          v30 = *v8;
          v31 = v8[1];
          v32 = nullptr;
          if ( *v8 != v31 )
          {
            while ( *(_DWORD *)v30 != 1869379180 )
            {
              v30 += 16;
              if ( v30 == v31 )
                goto LABEL_83;
            }
            if ( v30 == v31 )
              v32 = nullptr;
            else
              v32 = *(__int64 **)(v30 + 8);
          }
LABEL_83:
          if ( v32 != nullptr )
            v7 = v32;
          v42 = sub_140ED3970(a1 + 1, v7);
          if ( v42 < 0 )
            goto LABEL_88;
          v43 = *(_QWORD *)(*(_QWORD *)a1[1] + 8LL * (unsigned int)v42);
          if ( v43 == 0 )
            goto LABEL_88;
          return sub_1415630D0(*a1, v43, (unsigned int)v42);
        case 3u:
          LOBYTE(v7) = 1;
          v33 = *(_QWORD *)(a1[1] + 8LL) - *(_QWORD *)a1[1];
          if ( v33 != 0 )
          {
            v34 = (v33 >> 3) - 1;
            do
            {
              v35 = *(_QWORD *)(*(_QWORD *)a1[1] + 8 * v34);
              if ( v35 != 0 )
                sub_1415630D0(*a1, v35, v34);
              v14 = v34-- != 0;
            }
            while ( v14 );
          }
          return (unsigned int)v7;
        case 4u:
          v24 = *v8;
          v25 = v8[1];
          v26 = nullptr;
          if ( *v8 == v25 )
            goto LABEL_68;
          break;
        case 5u:
          sub_140DF3CB0(0);
          LOBYTE(v7) = 1;
          return (unsigned int)v7;
        default:
          goto LABEL_88;
      }
      while ( *(_DWORD *)v24 != 1869379180 )
      {
        v24 += 16;
        if ( v24 == v25 )
          goto LABEL_68;
      }
LABEL_61:
      if ( v24 == v25 )
        v26 = nullptr;
      else
        v26 = *(__int64 **)(v24 + 8);
LABEL_68:
      if ( v26 != nullptr )
        v7 = v26;
      v36 = *a1;
LABEL_71:
      LOBYTE(v7) = sub_141562520(v36, v7) != 0;
      return (unsigned int)v7;
    }
LABEL_88:
    LODWORD(v7) = 0;
    return (unsigned int)v7;
  }
  if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(v6 + 8))(v5, a2) != 11 )
    goto LABEL_88;
  v7 = (__int64 *)(*(__int64 (__fastcall **)(__int64 *, __int64 **, _QWORD))(**a2 + 184))(*a2, a2, 0);
  v12 = *(_QWORD *)(a1[1] + 8LL) - *(_QWORD *)a1[1];
  if ( v12 != 0 )
  {
    v13 = (v12 >> 3) - 1;
    do
    {
      v15 = *(_QWORD *)(*(_QWORD *)a1[1] + 8 * v13);
      if ( v15 != 0 )
        sub_1415630D0(*a1, v15, v13);
      v14 = v13-- != 0;
    }
    while ( v14 );
  }
  v16 = v7[1] - *v7;
  if ( v16 != 0 )
  {
    v17 = v16 >> 3;
    v18 = 1;
    if ( v17 >= 2 )
      v18 = v17;
    for ( i = 0; i != v18; ++i )
    {
      v20 = *(__int64 **)(*v7 + 8 * i);
      if ( v20 == nullptr )
        v20 = &qword_141B5A4A0;
      sub_141562520(*a1, v20);
    }
  }
  v21 = qword_141B60C38;
  v22 = qword_141B60C30;
  if ( qword_141B60C30 == qword_141B60C38 )
    goto LABEL_23;
  while ( *(_DWORD *)v22 != 1986359923 )
  {
    v22 += 16;
    if ( v22 == qword_141B60C38 )
      goto LABEL_23;
  }
  if ( v22 == qword_141B60C38 || (LOBYTE(v7) = 1, *(_QWORD *)(v22 + 8) == 0) )
  {
LABEL_23:
    LOBYTE(v7) = 1;
    LOBYTE(v21) = 1;
    sub_140DF3CB0(v21);
  }
  return (unsigned int)v7;
}
