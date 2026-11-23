__int64 __fastcall sub_140E4DEA0(__int64 **a1, __int64 **a2)
{
  __int64 *v2; // rbx
  char v5; // al
  __int64 *v6; // rcx
  __int64 v7; // rbp
  __int64 *v8; // rsi
  __int64 v9; // rax
  __int64 v10; // rcx
  __int64 v11; // rdx
  __int64 v12; // rdx
  __int64 v13; // rcx
  __int64 v14; // rax
  __int64 v15; // rdx
  __int64 v16; // rax
  unsigned __int64 v17; // rax
  __int64 v18; // rcx
  __int64 i; // r12
  __int64 *v20; // rsi
  __int64 **v21; // r13
  __int64 *v22; // rdi
  __int64 v23; // rax
  _QWORD *v24; // rsi
  __int64 v25; // r14
  __int64 v26; // r14
  __int64 v27; // r15
  __int64 *v28; // r8
  __int64 v29; // rcx
  __int64 v30; // rcx
  __int64 v31; // rcx
  __int64 v32; // rax
  __int64 *v33; // rdx
  __int64 *v34; // r14
  __int64 *v35; // rsi
  __int64 v36; // rax
  __int64 v37; // rcx
  _QWORD **v38; // rdi
  __int64 v39; // rax
  __int64 v40; // rcx
  __int64 *v41; // rdx
  __int64 v42; // rcx
  __int64 v43; // rdx
  __int64 *v44; // rax
  __int64 v45; // rdx
  __int64 v46; // rcx
  __int64 v47; // rax
  __int64 v48; // rdx
  __int64 v49; // rcx
  __int64 v50; // rcx
  __int64 v51; // rax
  __int64 v52; // rcx
  int v53; // eax
  __int64 v54; // rbx
  __int64 v55; // rbp
  __int64 v56; // rcx
  __int64 *v57; // rdx
  __int64 v58; // rax
  __int64 *v59; // rdi
  _QWORD **v60; // rdi
  int v61; // eax
  __int64 v62; // rax
  __int64 *v64; // rsi
  __int64 v65; // r15
  __int64 v66; // rax
  _QWORD *v67; // rdi
  __int64 v68; // rbp
  __int64 v69; // rbp
  __int64 v70; // rsi
  __int64 *v71; // r8
  unsigned int v72; // eax
  _QWORD *v73; // [rsp+28h] [rbp-50h]
  __int64 v74; // [rsp+30h] [rbp-48h]

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
        goto LABEL_100;
    }
    if ( v11 != v10 && *(_QWORD *)(v11 + 8) != 0 )
    {
      v33 = nullptr;
      while ( *(_DWORD *)v9 != 1819504496 )
      {
        v9 += 16;
        if ( v9 == v10 )
          goto LABEL_47;
      }
      if ( v9 == v10 )
        v33 = nullptr;
      else
        v33 = *(__int64 **)(v9 + 8);
LABEL_47:
      v34 = &qword_141B5A4A0;
      if ( v33 == nullptr )
        v33 = &qword_141B5A4A0;
      switch ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)*v33 + 64LL))(*v33) )
      {
        case 0u:
          v35 = *a1;
          v36 = sub_140F72410(160);
          v37 = *v35;
          *(_QWORD *)(v36 + 8) = -1;
          *(_DWORD *)(v36 + 16) = 0;
          *(_QWORD *)v36 = 0x14188DD98LL;
          *(_QWORD *)(v36 + 24) = v37;
          *(_QWORD *)(v36 + 40) = 0;
          *(_QWORD *)(v36 + 64) = 0;
          *(_QWORD *)(v36 + 56) = 0;
          *(_QWORD *)(v36 + 96) = 0;
          *(_QWORD *)(v36 + 88) = 0;
          *(_QWORD *)(v36 + 80) = 0;
          *(_QWORD *)(v36 + 120) = -1;
          *(_QWORD *)(v36 + 112) = -1;
          *(_QWORD *)(v36 + 104) = -1;
          *(_QWORD *)(v36 + 128) = 0;
          *(_DWORD *)(v36 + 136) = 0;
          *(_WORD *)(v36 + 140) = -1;
          *(_QWORD *)(v36 + 142) = 0;
          *(_QWORD *)(v36 + 150) = 0;
          *(_BYTE *)(v36 + 158) = 0;
          *(_QWORD *)(v36 + 32) = -(__int64)((*(_BYTE *)(qword_141B5FE08 + 90) & 4) == 0);
          *(_QWORD *)(v36 + 48) = -(__int64)((*(_BYTE *)(qword_141B5FE08 + 90) & 4) == 0);
          *(_QWORD *)(v36 + 72) = -(__int64)((*(_BYTE *)(qword_141B5FE08 + 90) & 4) == 0);
          sub_140F4A860(&qword_141B5FDA8, 12, v36, 0xFFFFFFFFLL);
          LOBYTE(v2) = 1;
          return (unsigned int)v2;
        case 1u:
          v38 = a1 + 1;
          v39 = *v8;
          v40 = v8[1];
          v41 = nullptr;
          if ( *v8 != v40 )
          {
            while ( *(_DWORD *)v39 != 1869379180 )
            {
              v39 += 16;
              if ( v39 == v40 )
                goto LABEL_82;
            }
            if ( v39 == v40 )
              v41 = nullptr;
            else
              v41 = *(__int64 **)(v39 + 8);
          }
LABEL_82:
          if ( v41 == nullptr )
            v41 = &qword_141B5A4A0;
          v53 = sub_140E4E790(v38, v41);
          if ( v53 < 0 )
            goto LABEL_100;
          v54 = *(_QWORD *)(**v38 + 8LL * (unsigned int)v53);
          if ( v54 == 0 )
            goto LABEL_100;
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
                goto LABEL_112;
            }
            if ( v58 == v56 )
              v57 = nullptr;
            else
              v57 = *(__int64 **)(v58 + 8);
LABEL_112:
            v59 = &qword_141B5A4A0;
            if ( v57 != nullptr )
              v59 = v57;
            v57 = nullptr;
            while ( *(_DWORD *)v55 != 1768169504 )
            {
              v55 += 16;
              if ( v55 == v56 )
                goto LABEL_121;
            }
            if ( v55 == v56 )
              v57 = nullptr;
            else
              v57 = *(__int64 **)(v55 + 8);
          }
LABEL_121:
          if ( v57 != nullptr )
            v34 = v57;
          v72 = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v34 + 80LL))(*v34, v34);
          return sub_14118F5F0(v54, v72, v59);
        case 2u:
          v42 = *v8;
          v43 = v8[1];
          v44 = nullptr;
          if ( *v8 != v43 )
          {
            while ( *(_DWORD *)v42 != 1869379180 )
            {
              v42 += 16;
              if ( v42 == v43 )
                goto LABEL_95;
            }
            if ( v42 == v43 )
              v44 = nullptr;
            else
              v44 = *(__int64 **)(v42 + 8);
          }
LABEL_95:
          if ( v44 != nullptr )
            v34 = v44;
          v60 = a1 + 1;
          v61 = sub_140E4E790(v60, v34);
          if ( v61 < 0 )
            goto LABEL_100;
          v62 = *(_QWORD *)(**v60 + 8LL * (unsigned int)v61);
          if ( v62 == 0 )
            goto LABEL_100;
          *(_QWORD *)(v62 + 24) = 0;
          LOBYTE(v2) = 1;
          return (unsigned int)v2;
        case 3u:
          LOBYTE(v2) = 1;
          v45 = a1[1][1] - *a1[1];
          if ( v45 != 0 )
          {
            v46 = v45 >> 3;
            v47 = v45 >> 3;
            if ( (v45 & 8) != 0 )
            {
              v47 = v46 - 1;
              v48 = *(_QWORD *)(*a1[1] + 8 * v46 - 8);
              if ( v48 != 0 )
                *(_QWORD *)(v48 + 24) = 0;
            }
            if ( v46 != 1 )
            {
              do
              {
                v49 = *(_QWORD *)(*a1[1] + 8 * v47 - 8);
                if ( v49 != 0 )
                  *(_QWORD *)(v49 + 24) = 0;
                v50 = *(_QWORD *)(*a1[1] + 8 * v47 - 16);
                v47 -= 2;
                if ( v50 != 0 )
                  *(_QWORD *)(v50 + 24) = 0;
              }
              while ( v47 != 0 );
            }
          }
          return (unsigned int)v2;
        case 4u:
          v51 = *v8;
          v52 = v8[1];
          v2 = nullptr;
          if ( *v8 == v52 )
            goto LABEL_103;
          break;
        case 5u:
          sub_140DF3CB0(0);
          LOBYTE(v2) = 1;
          return (unsigned int)v2;
        default:
          goto LABEL_100;
      }
      while ( *(_DWORD *)v51 != 1869379180 )
      {
        v51 += 16;
        if ( v51 == v52 )
          goto LABEL_103;
      }
      if ( v51 == v52 )
        v2 = nullptr;
      else
        v2 = *(__int64 **)(v51 + 8);
LABEL_103:
      if ( v2 == nullptr )
        v2 = &qword_141B5A4A0;
      v64 = *a1;
      v65 = sub_140F72410(160);
      v66 = *v64;
      *(_QWORD *)(v65 + 8) = -1;
      *(_DWORD *)(v65 + 16) = 0;
      *(_QWORD *)v65 = 0x14188DD98LL;
      *(_QWORD *)(v65 + 24) = v66;
      *(_QWORD *)(v65 + 40) = 0;
      *(_QWORD *)(v65 + 64) = 0;
      *(_QWORD *)(v65 + 56) = 0;
      *(_QWORD *)(v65 + 96) = 0;
      *(_QWORD *)(v65 + 88) = 0;
      *(_QWORD *)(v65 + 80) = 0;
      *(_QWORD *)(v65 + 120) = -1;
      *(_QWORD *)(v65 + 112) = -1;
      *(_QWORD *)(v65 + 104) = -1;
      *(_QWORD *)(v65 + 128) = 0;
      *(_DWORD *)(v65 + 136) = 0;
      *(_WORD *)(v65 + 140) = -1;
      *(_QWORD *)(v65 + 142) = 0;
      *(_QWORD *)(v65 + 150) = 0;
      *(_BYTE *)(v65 + 158) = 0;
      *(_QWORD *)(v65 + 32) = -(__int64)((*(_BYTE *)(qword_141B5FE08 + 90) & 4) == 0);
      *(_QWORD *)(v65 + 48) = -(__int64)((*(_BYTE *)(qword_141B5FE08 + 90) & 4) == 0);
      *(_QWORD *)(v65 + 72) = -(__int64)((*(_BYTE *)(qword_141B5FE08 + 90) & 4) == 0);
      sub_140F4A860(&qword_141B5FDA8, 12, v65, 0xFFFFFFFFLL);
      v67 = (_QWORD *)(*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(*(_QWORD *)*v2 + 176LL))(*v2, v2, 0);
      LOBYTE(v2) = 1;
      v68 = v67[1] - *v67;
      if ( v68 != 0 )
      {
        v69 = v68 >> 4;
        v70 = 8;
        do
        {
          v71 = *(__int64 **)(*v67 + v70);
          if ( v71 == nullptr )
            v71 = &qword_141B5A4A0;
          sub_14118F5F0(v65, *(unsigned int *)(*v67 + v70 - 8), v71);
          v70 += 16;
          --v69;
        }
        while ( v69 != 0 );
      }
      return (unsigned int)v2;
    }
LABEL_100:
    LODWORD(v2) = 0;
    return (unsigned int)v2;
  }
  if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(v7 + 8))(v6, a2) != 11 )
    goto LABEL_100;
  v73 = (_QWORD *)(*(__int64 (__fastcall **)(__int64 *, __int64 **, _QWORD))(**a2 + 184))(*a2, a2, 0);
  v12 = a1[1][1] - *a1[1];
  if ( v12 != 0 )
  {
    v13 = v12 >> 3;
    v14 = v12 >> 3;
    if ( (v12 & 8) != 0 )
    {
      v14 = v13 - 1;
      v15 = *(_QWORD *)(*a1[1] + 8 * v13 - 8);
      if ( v15 != 0 )
        *(_QWORD *)(v15 + 24) = 0;
    }
    if ( v13 != 1 )
    {
      do
      {
        v29 = *(_QWORD *)(*a1[1] + 8 * v14 - 8);
        if ( v29 != 0 )
          *(_QWORD *)(v29 + 24) = 0;
        v30 = *(_QWORD *)(*a1[1] + 8 * v14 - 16);
        v14 -= 2;
        if ( v30 != 0 )
          *(_QWORD *)(v30 + 24) = 0;
      }
      while ( v14 != 0 );
    }
  }
  v16 = v73[1] - *v73;
  if ( v16 != 0 )
  {
    v17 = v16 >> 3;
    v18 = 1;
    if ( v17 >= 2 )
      v18 = v17;
    v74 = v18;
    for ( i = 0; i != v74; ++i )
    {
      v20 = *(__int64 **)(*v73 + 8 * i);
      if ( v20 == nullptr )
        v20 = &qword_141B5A4A0;
      v21 = a1;
      v22 = *a1;
      v2 = (__int64 *)sub_140F72410(160);
      v23 = *v22;
      v2[1] = -1;
      *((_DWORD *)v2 + 4) = 0;
      *v2 = 0x14188DD98LL;
      v2[3] = v23;
      v2[5] = 0;
      v2[8] = 0;
      v2[7] = 0;
      v2[12] = 0;
      v2[11] = 0;
      v2[10] = 0;
      v2[15] = -1;
      v2[14] = -1;
      v2[13] = -1;
      v2[16] = 0;
      *((_DWORD *)v2 + 34) = 0;
      *((_WORD *)v2 + 70) = -1;
      *(__int64 *)((char *)v2 + 142) = 0;
      *(__int64 *)((char *)v2 + 150) = 0;
      *((_BYTE *)v2 + 158) = 0;
      v2[4] = -(__int64)((*(_BYTE *)(qword_141B5FE08 + 90) & 4) == 0);
      v2[6] = -(__int64)((*(_BYTE *)(qword_141B5FE08 + 90) & 4) == 0);
      v2[9] = -(__int64)((*(_BYTE *)(qword_141B5FE08 + 90) & 4) == 0);
      sub_140F4A860(&qword_141B5FDA8, 12, v2, 0xFFFFFFFFLL);
      v24 = (_QWORD *)(*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(*(_QWORD *)*v20 + 176LL))(*v20, v20, 0);
      v25 = v24[1] - *v24;
      if ( v25 != 0 )
      {
        v26 = v25 >> 4;
        v27 = 8;
        do
        {
          v28 = *(__int64 **)(*v24 + v27);
          if ( v28 == nullptr )
            v28 = &qword_141B5A4A0;
          sub_14118F5F0(v2, *(unsigned int *)(*v24 + v27 - 8), v28);
          v27 += 16;
          --v26;
        }
        while ( v26 != 0 );
      }
      a1 = v21;
    }
  }
  v31 = qword_141B60C38;
  v32 = qword_141B60C30;
  if ( qword_141B60C30 == qword_141B60C38 )
    goto LABEL_34;
  while ( *(_DWORD *)v32 != 1986359923 )
  {
    v32 += 16;
    if ( v32 == qword_141B60C38 )
      goto LABEL_34;
  }
  if ( v32 == qword_141B60C38 || (LOBYTE(v2) = 1, *(_QWORD *)(v32 + 8) == 0) )
  {
LABEL_34:
    LOBYTE(v2) = 1;
    LOBYTE(v31) = 1;
    sub_140DF3CB0(v31);
  }
  return (unsigned int)v2;
}
