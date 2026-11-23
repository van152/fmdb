bool __fastcall sub_141400230(__int64 *a1, _QWORD *a2)
{
  __int64 v4; // rbx
  __int64 v6; // r14
  unsigned __int8 v7; // al
  __int64 v8; // r13
  __int64 v9; // r8
  __int64 v10; // rsi
  __int64 v11; // rdx
  unsigned __int64 v12; // rbx
  __int64 v13; // rcx
  __int64 v14; // rsi
  __int64 v15; // rdi
  __int64 v16; // r8
  __int64 v17; // r13
  __int64 v18; // rcx
  _QWORD *v19; // rax
  char *v20; // rbx
  unsigned __int64 v21; // rdi
  unsigned __int64 v22; // rdx
  unsigned __int64 v23; // rcx
  unsigned __int64 v24; // rsi
  __int64 v25; // rcx
  __int64 v26; // rcx
  __int64 v27; // rsi
  __int64 v28; // rcx
  unsigned __int64 v29; // rcx
  unsigned __int64 v30; // rdx
  __int64 v31; // rdi
  unsigned __int64 v32; // rax
  _DWORD *v33; // r10
  unsigned __int64 v34; // r8
  __int64 v35; // rdi
  unsigned __int64 v36; // rbx
  __int128 v37; // xmm0
  __int64 v38; // rbx
  __int64 v39; // rdi
  __int128 v40; // xmm0
  unsigned __int64 v41; // rdx
  __int64 v42; // rsi
  __int128 v43; // xmm0
  __int64 v44; // rdx
  __int64 v45; // rbx
  __int128 v46; // xmm0
  __int64 v47; // rdx
  _DWORD *v48; // rsi
  __int64 v49; // rdx
  __int64 v50; // rsi
  __int64 v51; // r8
  __int64 v52; // rax
  __int64 v53; // rdx
  __int64 v54; // rbx
  __int64 v55; // rdi
  __int64 v56; // rbx
  __int64 v57; // rbx
  __int64 v58; // rbx
  __int64 v59; // rbx
  __int64 v60; // rdi
  __int64 v61; // rbx
  __int64 *v62; // rdx
  __int64 v63; // rsi
  __int64 v64; // rdi
  __int64 v65; // rax
  __int64 v66; // rcx
  unsigned __int64 v67; // [rsp+28h] [rbp-28h]
  int v68; // [rsp+30h] [rbp-20h]
  __int64 v69; // [rsp+30h] [rbp-20h]
  __int64 v70; // [rsp+38h] [rbp-18h] BYREF
  int v71; // [rsp+40h] [rbp-10h]
  unsigned __int8 v72; // [rsp+4Fh] [rbp-1h] BYREF
  __int64 v73; // [rsp+50h] [rbp+0h]

  v73 = -2;
  v4 = *a2;
  (*(void (__fastcall **)(_QWORD, unsigned __int8 *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v72, a3: 1);
  if ( *(_DWORD *)(v4 + 16) != 0 )
    return false;
  v6 = *a2;
  if ( *a2 != 0 )
    _InterlockedIncrement((volatile signed __int32 *)(v6 + 8));
  sub_1411FF180(a1, a2: v72, a3: &v70);
  v7 = v72;
  if ( v72 != 0 )
  {
    v8 = 0;
    v9 = 0;
    v10 = 0;
    v11 = 0;
    v12 = 0;
    do
    {
      v13 = v10;
      v14 = *a1 + 16 * v12;
      v15 = v8 + *a1;
      if ( v15 == v13 )
      {
        v9 += 16;
      }
      else
      {
        if ( v9 != 0 && v6 != 0 )
        {
          (*(void (__fastcall **)(__int64, __int64))(*(_QWORD *)v6 + 40LL))(a1: v6, a2: v11);
          v7 = v72;
        }
        v11 = v15;
        v9 = 16;
      }
      v10 = v14 + 16;
      ++v12;
      v8 += 16;
    }
    while ( v12 < v7 );
    if ( v9 != 0 && v6 != 0 )
      (*(void (__fastcall **)(__int64, __int64))(*(_QWORD *)v6 + 40LL))(a1: v6, a2: v11);
  }
  (*(void (__fastcall **)(__int64, __int64 *, __int64))(*(_QWORD *)v6 + 40LL))(a1: v6, a2: &v70, a3: 4);
  if ( *(_DWORD *)(v6 + 16) != 0 || (v17 = (unsigned int)v70, (int)v70 < 0) )
  {
    if ( _InterlockedDecrement((volatile signed __int32 *)(v6 + 8)) == 0 )
      (**(void (__fastcall ***)(__int64, __int64))v6)(a1: v6, a2: 1);
    return false;
  }
  v18 = a1[3];
  v19 = (_QWORD *)a1[4];
  v20 = (char *)v19 - v18;
  v21 = ((__int64)v19 - v18) >> 3;
  if ( v21 > (unsigned int)v70 )
  {
    v19 = (_QWORD *)(v18 + 8LL * (unsigned int)v70);
    goto LABEL_23;
  }
  if ( v21 < (unsigned int)v70 )
  {
    v22 = (a1[5] - v18) >> 3;
    if ( v22 >= (unsigned int)v70 )
    {
      v29 = (unsigned int)v70 - v21;
      if ( (unsigned int)v70 != v21 )
      {
        if ( v29 >= 4 )
        {
          v30 = v29 & 0xFFFFFFFFFFFFFFFCuLL;
          if ( (v29 & 0xFFFFFFFFFFFFFFFCuLL) - 4 >= 0xC )
          {
            v36 = ((((v29 & 0xFFFFFFFFFFFFFFFCuLL) - 4) >> 2) + 1) & 0x7FFFFFFFFFFFFFFCLL;
            v31 = 0;
            v37 = MEMORY[0x14178BBF0];
            do
            {
              *(_OWORD *)&v19[v31] = v37;
              *(_OWORD *)&v19[v31 + 2] = v37;
              *(_OWORD *)&v19[v31 + 4] = v37;
              *(_OWORD *)&v19[v31 + 6] = v37;
              *(_OWORD *)&v19[v31 + 8] = v37;
              *(_OWORD *)&v19[v31 + 10] = v37;
              *(_OWORD *)&v19[v31 + 12] = v37;
              *(_OWORD *)&v19[v31 + 14] = v37;
              v31 += 16;
              v36 -= 4LL;
            }
            while ( v36 != 0 );
          }
          else
          {
            v31 = 0;
          }
          if ( (((unsigned __int8)(((v29 & 0xFFFFFFFFFFFFFFFCuLL) - 4) >> 2) + 1) & 3) != 0 )
          {
            v38 = (__int64)&v19[v31 + 2];
            v39 = 0;
            v40 = MEMORY[0x14178BBF0];
            do
            {
              *(_OWORD *)(v38 + v39 - 16) = v40;
              *(_OWORD *)(v38 + v39) = v40;
              v39 += 32;
            }
            while ( 32LL * (((unsigned __int8)(((v29 & 0xFFFFFFFFFFFFFFFCuLL) - 4) >> 2) + 1) & 3) != v39 );
          }
          v19 += v30;
          if ( v29 == v30 )
            goto LABEL_23;
          v29 &= 3u;
        }
        do
        {
          *v19++ = 0xFFFFFFFFLL;
          --v29;
        }
        while ( v29 != 0 );
      }
LABEL_23:
      a1[4] = (__int64)v19;
      goto LABEL_64;
    }
    v23 = v22 + (v22 >> 1);
    if ( v23 <= (unsigned int)v70 )
      v23 = (unsigned int)v70;
    v67 = v23;
    v24 = 8 * v23;
    if ( *(_BYTE *)(qword_141ABE200 + 52) != 0
      && (v25 = *(_QWORD *)(qword_141ABE200 + 24), (*(_QWORD *)(qword_141ABE200 + 32) - v25) >> 3 > v24)
      && (v26 = *(_QWORD *)(v25 + 8 * v24)) != 0 )
    {
      v68 = v24;
      v27 = *(unsigned int *)(v26 + 88);
      v28 = sub_1407E58C0(a1: v26, a2: *(unsigned int *)(v26 + 80));
      if ( v27 != 0 )
      {
        *(_DWORD *)v28 = v68;
        v28 += v27;
      }
    }
    else
    {
      v69 = *(unsigned int *)(qword_141ABE200 + 48);
      v28 = sub_141601260(a1: (unsigned int)(v69 + v24), a2: 4096, a3: v16);
      if ( v69 != 0 )
      {
        *(_DWORD *)v28 = v24;
        v28 += v69;
      }
    }
    v32 = v17 - v21;
    if ( v17 == v21 )
      goto LABEL_61;
    v33 = (_DWORD *)(v28 + 8 * v21);
    if ( v32 >= 4 )
    {
      v34 = v32 & 0xFFFFFFFFFFFFFFFCuLL;
      if ( (v32 & 0xFFFFFFFFFFFFFFFCuLL) - 4 >= 0xC )
      {
        v41 = ((((v32 & 0xFFFFFFFFFFFFFFFCuLL) - 4) >> 2) + 1) & 0x7FFFFFFFFFFFFFFCLL;
        v42 = (__int64)&v20[v28 + 112];
        v35 = 0;
        v43 = MEMORY[0x14178BBF0];
        do
        {
          *(_OWORD *)&v20[8 * v35 + v28] = v43;
          *(_OWORD *)(v42 + 8 * v35 - 96) = v43;
          *(_OWORD *)(v42 + 8 * v35 - 80) = v43;
          *(_OWORD *)(v42 + 8 * v35 - 64) = v43;
          *(_OWORD *)(v42 + 8 * v35 - 48) = v43;
          *(_OWORD *)(v42 + 8 * v35 - 32) = v43;
          *(_OWORD *)(v42 + 8 * v35 - 16) = v43;
          *(_OWORD *)(v42 + 8 * v35) = v43;
          v35 += 16;
          v41 -= 4LL;
        }
        while ( v41 != 0 );
      }
      else
      {
        v35 = 0;
      }
      if ( (((unsigned __int8)(((v32 & 0xFFFFFFFFFFFFFFFCuLL) - 4) >> 2) + 1) & 3) != 0 )
      {
        v44 = (__int64)&v20[8 * v35 + 16 + v28];
        v45 = 0;
        v46 = MEMORY[0x14178BBF0];
        do
        {
          *(_OWORD *)(v44 + v45 - 16) = v46;
          *(_OWORD *)(v44 + v45) = v46;
          v45 += 32;
        }
        while ( 32LL * (((unsigned __int8)(((v32 & 0xFFFFFFFFFFFFFFFCuLL) - 4) >> 2) + 1) & 3) != v45 );
      }
      if ( v32 == v34 )
        goto LABEL_61;
      v32 &= 3u;
      v33 += 2 * v34;
    }
    v47 = 0;
    do
      *(_QWORD *)&v33[2 * v47++] = 0xFFFFFFFFLL;
    while ( v32 != v47 );
LABEL_61:
    v48 = (_DWORD *)v28;
    sub_141758A00(a1: v28, a2: a1[3], a3: a1[4] - a1[3]);
    v49 = a1[3];
    if ( v49 != 0 )
      sub_1407E6420(a1: qword_141ABE200, a2: v49, a3: a1[5] - v49);
    a1[3] = (__int64)v48;
    a1[4] = (__int64)&v48[2 * v17];
    a1[5] = (__int64)&v48[2 * v67];
    LODWORD(v17) = v70;
  }
LABEL_64:
  if ( (int)v17 > 0 )
  {
    v50 = 0;
    v51 = 0;
    v52 = 0;
    v53 = 0;
    v54 = 0;
    do
    {
      v55 = a1[3];
      if ( v55 + v50 == v52 )
      {
        v51 += 7;
      }
      else
      {
        if ( v51 != 0 )
        {
          (*(void (__fastcall **)(__int64, __int64))(*(_QWORD *)v6 + 40LL))(a1: v6, a2: v53);
          LODWORD(v17) = v70;
        }
        v53 = v55 + v50;
        v51 = 7;
      }
      v52 = v55 + 8 * v54++ + 7;
      v50 += 8;
    }
    while ( v54 < (int)v17 );
    if ( v51 != 0 )
      (*(void (__fastcall **)(__int64, __int64))(*(_QWORD *)v6 + 40LL))(a1: v6, a2: v53);
  }
  if ( _InterlockedDecrement((volatile signed __int32 *)(v6 + 8)) == 0 )
    (**(void (__fastcall ***)(__int64, __int64))v6)(a1: v6, a2: 1);
  v56 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: (__int64)a1 + 73, a3: 1);
  if ( *(_DWORD *)(v56 + 16) != 0 )
    return false;
  v57 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: (__int64)a1 + 74, a3: 1);
  if ( *(_DWORD *)(v57 + 16) != 0 )
    return false;
  v58 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64 *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 9, a3: 1);
  if ( *(_DWORD *)(v58 + 16) != 0 )
    return false;
  v59 = *a2;
  (*(void (__fastcall **)(_QWORD, unsigned __int8 *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v72, a3: 1);
  if ( *(_DWORD *)(v59 + 16) != 0 )
    return false;
  if ( (unsigned __int8)sub_140087070() != 0 )
  {
    sub_141400860(a1: a1 + 6, a2: v72);
    if ( v72 != 0 )
    {
      v60 = 0;
      do
      {
        v61 = sub_141400910();
        *(_QWORD *)v61 = 0;
        *(_DWORD *)(v61 + 8) = 0;
        v70 = v61;
        if ( (unsigned __int8)sub_1414009C0(a1: v61, a2) == 0 )
          return false;
        v62 = (__int64 *)a1[7];
        if ( v62 == (__int64 *)a1[8] )
        {
          sub_141405030(a1: a1 + 6, a2: v62, a3: &v70);
        }
        else
        {
          *v62 = v61;
          a1[7] += 8;
        }
      }
      while ( ++v60 < (unsigned __int64)v72 );
    }
  }
  else if ( v72 != 0 )
  {
    v63 = 0;
    do
    {
      v71 = 0;
      v70 = 0;
      if ( (unsigned __int8)sub_1414009C0(a1: &v70, a2) == 0 )
        return false;
    }
    while ( ++v63 < (unsigned __int64)v72 );
  }
  if ( (unsigned __int16)qword_141B60330 < 0xDF0u )
  {
    v65 = *a1;
    v66 = a1[1];
    while ( v65 != v66 )
    {
      if ( (unsigned __int8)(*(_BYTE *)(v65 + 11) - 11) <= 1u )
        ++*((_BYTE *)a1 + 75);
      v65 += 16;
    }
    return true;
  }
  v64 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: (__int64)a1 + 75, a3: 1);
  return *(_DWORD *)(v64 + 16) == 0;
}
