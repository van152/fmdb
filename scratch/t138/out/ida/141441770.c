bool __fastcall sub_141441770(_QWORD *a1, _QWORD *a2)
{
  __int64 v4; // rdi
  __int64 v5; // rdi
  __int64 v7; // rbx
  __int64 v8; // rbp
  __int64 v9; // rbp
  __int64 v10; // rbp
  __int64 v11; // rbp
  __int64 v12; // rdi
  __int64 v13; // rax
  __int64 v14; // rbx
  __int64 v15; // rbp
  __int64 v16; // rbp
  __int64 v17; // rbp
  __int64 v18; // rdi
  __int64 v19; // rax
  __int64 v20; // rbx
  __int64 v21; // rbp
  __int64 v22; // rbp
  __int64 v23; // rbp
  __int64 v24; // rdi
  __int64 v25; // rax
  __int64 v26; // rbx
  __int64 v27; // rbp
  __int64 v28; // rbp
  __int64 v29; // rbp
  __int64 v30; // rdi
  __int64 v31; // rax
  __int64 v32; // rbx
  __int64 v33; // rbp
  __int64 v34; // rbp
  __int64 v35; // rbp
  __int64 v36; // rdi
  __int64 v37; // rax
  __int64 v38; // r15
  __int64 v39; // rbp
  __int64 v40; // rbp
  __int64 v41; // rbp
  __int64 v42; // rax
  __int64 v43; // rdi
  __int64 v44; // rdi
  __int64 v45; // rdi
  __int64 v46; // rdi
  __int64 v47; // rdi
  __int64 v48; // rdi
  unsigned __int8 v49; // [rsp+25h] [rbp-63h] BYREF
  char v50; // [rsp+26h] [rbp-62h] BYREF
  char v51; // [rsp+27h] [rbp-61h] BYREF
  int v52; // [rsp+28h] [rbp-60h] BYREF
  _DWORD v53[4]; // [rsp+2Ch] [rbp-5Ch] BYREF
  __int64 v54; // [rsp+3Ch] [rbp-4Ch]
  __int16 v55; // [rsp+44h] [rbp-44h]
  char v56; // [rsp+46h] [rbp-42h]

  v51 = 0;
  v4 = *a2;
  (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v51, a3: 1);
  if ( *(_DWORD *)(v4 + 16) != 0 )
    return false;
  v49 = 0;
  v5 = *a2;
  (*(void (__fastcall **)(_QWORD, unsigned __int8 *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v49, a3: 1);
  if ( *(_DWORD *)(v5 + 16) != 0 )
    return false;
  if ( *a1 != a1[1] )
    a1[1] = *a1;
  if ( v49 != 0 )
  {
    v7 = 0;
    do
    {
      v52 = 0;
      LOBYTE(v53[0]) = 0;
      LOBYTE(v53[1]) = 1;
      v8 = *a2;
      (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v50, a3: 1);
      if ( *(_DWORD *)(v8 + 16) != 0 )
        return false;
      v9 = *a2;
      (*(void (__fastcall **)(_QWORD, int *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v52, a3: 4);
      if ( *(_DWORD *)(v9 + 16) != 0 )
        return false;
      v10 = *a2;
      (*(void (__fastcall **)(_QWORD, _DWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v53, a3: 1);
      if ( *(_DWORD *)(v10 + 16) != 0 )
        return false;
      v11 = *a2;
      (*(void (__fastcall **)(_QWORD, _DWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v53[1], a3: 1);
      if ( *(_DWORD *)(v11 + 16) != 0 || *(_DWORD *)(*a2 + 16LL) != 0 )
        return false;
      sub_141441EC0(a1, a2: &v52);
    }
    while ( ++v7 < (unsigned __int64)v49 );
  }
  v49 = 0;
  v12 = *a2;
  (*(void (__fastcall **)(_QWORD, unsigned __int8 *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v49, a3: 1);
  if ( *(_DWORD *)(v12 + 16) != 0 )
    return false;
  v13 = a1[3];
  if ( v13 != a1[4] )
    a1[4] = v13;
  if ( v49 != 0 )
  {
    v14 = 0;
    do
    {
      v52 = 0;
      LOBYTE(v53[0]) = 0;
      v15 = *a2;
      (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v50, a3: 1);
      if ( *(_DWORD *)(v15 + 16) != 0 )
        return false;
      v16 = *a2;
      (*(void (__fastcall **)(_QWORD, int *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v52, a3: 4);
      if ( *(_DWORD *)(v16 + 16) != 0 )
        return false;
      v17 = *a2;
      (*(void (__fastcall **)(_QWORD, _DWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v53, a3: 1);
      if ( *(_DWORD *)(v17 + 16) != 0 )
        return false;
      sub_141442090(a1, a2: &v52);
    }
    while ( ++v14 < (unsigned __int64)v49 );
  }
  v49 = 0;
  v18 = *a2;
  (*(void (__fastcall **)(_QWORD, unsigned __int8 *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v49, a3: 1);
  if ( *(_DWORD *)(v18 + 16) != 0 )
    return false;
  v19 = a1[6];
  if ( v19 != a1[7] )
    a1[7] = v19;
  if ( v49 != 0 )
  {
    v20 = 0;
    do
    {
      v52 = 0;
      LOBYTE(v53[0]) = 0;
      v21 = *a2;
      (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v50, a3: 1);
      if ( *(_DWORD *)(v21 + 16) != 0 )
        return false;
      v22 = *a2;
      (*(void (__fastcall **)(_QWORD, int *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v52, a3: 4);
      if ( *(_DWORD *)(v22 + 16) != 0 )
        return false;
      v23 = *a2;
      (*(void (__fastcall **)(_QWORD, _DWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v53, a3: 1);
      if ( *(_DWORD *)(v23 + 16) != 0 )
        return false;
      sub_141442250(a1, a2: &v52);
    }
    while ( ++v20 < (unsigned __int64)v49 );
  }
  v49 = 0;
  v24 = *a2;
  (*(void (__fastcall **)(_QWORD, unsigned __int8 *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v49, a3: 1);
  if ( *(_DWORD *)(v24 + 16) != 0 )
    return false;
  v25 = a1[9];
  if ( v25 != a1[10] )
    a1[10] = v25;
  if ( v49 != 0 )
  {
    v26 = 0;
    do
    {
      v52 = 0;
      LOBYTE(v53[0]) = 0;
      v27 = *a2;
      (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v50, a3: 1);
      if ( *(_DWORD *)(v27 + 16) != 0 )
        return false;
      v28 = *a2;
      (*(void (__fastcall **)(_QWORD, int *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v52, a3: 4);
      if ( *(_DWORD *)(v28 + 16) != 0 )
        return false;
      v29 = *a2;
      (*(void (__fastcall **)(_QWORD, _DWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v53, a3: 1);
      if ( *(_DWORD *)(v29 + 16) != 0 )
        return false;
      sub_141442410(a1, a2: &v52);
    }
    while ( ++v26 < (unsigned __int64)v49 );
  }
  v49 = 0;
  v30 = *a2;
  (*(void (__fastcall **)(_QWORD, unsigned __int8 *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v49, a3: 1);
  if ( *(_DWORD *)(v30 + 16) != 0 )
    return false;
  v31 = a1[12];
  if ( v31 != a1[13] )
    a1[13] = v31;
  if ( v49 != 0 )
  {
    v32 = 0;
    do
    {
      v52 = 0;
      LOBYTE(v53[0]) = 0;
      v33 = *a2;
      (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v50, a3: 1);
      if ( *(_DWORD *)(v33 + 16) != 0 )
        return false;
      v34 = *a2;
      (*(void (__fastcall **)(_QWORD, int *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v52, a3: 4);
      if ( *(_DWORD *)(v34 + 16) != 0 )
        return false;
      v35 = *a2;
      (*(void (__fastcall **)(_QWORD, _DWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v53, a3: 1);
      if ( *(_DWORD *)(v35 + 16) != 0 )
        return false;
      sub_1414425B0(a1, a2: &v52);
    }
    while ( ++v32 < (unsigned __int64)v49 );
  }
  v49 = 0;
  v36 = *a2;
  (*(void (__fastcall **)(_QWORD, unsigned __int8 *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v49, a3: 1);
  if ( *(_DWORD *)(v36 + 16) != 0 )
    return false;
  v37 = a1[15];
  if ( v37 != a1[16] )
    a1[16] = v37;
  if ( v49 != 0 )
  {
    v38 = 0;
    do
    {
      v52 = 0;
      LOBYTE(v53[0]) = 0;
      *(_QWORD *)&v53[1] = 0x76C0001076C0001LL;
      v39 = *a2;
      (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v50, a3: 1);
      if ( *(_DWORD *)(v39 + 16) != 0 )
        return false;
      v40 = *a2;
      (*(void (__fastcall **)(_QWORD, int *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v52, a3: 4);
      if ( *(_DWORD *)(v40 + 16) != 0 )
        return false;
      v41 = *a2;
      (*(void (__fastcall **)(_QWORD, _DWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v53, a3: 1);
      if ( *(_DWORD *)(v41 + 16) != 0
        || (unsigned __int8)sub_140DB8980(a1: &v53[1], a2) == 0
        || (unsigned __int8)sub_140DB8980(a1: &v53[2], a2) == 0
        || *(_DWORD *)(*a2 + 16LL) != 0 )
      {
        return false;
      }
      sub_141442770(a1, a2: &v52);
    }
    while ( ++v38 < (unsigned __int64)v49 );
  }
  v42 = a1[18];
  if ( v42 != a1[19] )
    a1[19] = v42;
  v43 = *a2;
  (*(void (__fastcall **)(_QWORD, unsigned __int8 *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v49, a3: 1);
  if ( *(_DWORD *)(v43 + 16) != 0 )
    return false;
  if ( v49 != 0 )
  {
    v44 = 0;
    do
    {
      v52 = 124518401;
      memset(v53, 255, 13);
      v54 = 0xFFFFFFFFLL;
      v55 = -1;
      v56 = 0;
      if ( (unsigned __int8)sub_14156ADD0(a1: &v52, a2) == 0 )
        return false;
      sub_14103AF20(a1: a1 + 18, a2: &v52);
    }
    while ( ++v44 < (unsigned __int64)v49 );
  }
  v45 = *a2;
  (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 21, a3: 4);
  if ( *(_DWORD *)(v45 + 16) != 0 )
    return false;
  v46 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: (__int64)a1 + 172, a3: 1);
  if ( *(_DWORD *)(v46 + 16) != 0 )
    return false;
  v47 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: (__int64)a1 + 173, a3: 1);
  if ( *(_DWORD *)(v47 + 16) != 0 )
    return false;
  v48 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: (__int64)a1 + 174, a3: 1);
  if ( *(_DWORD *)(v48 + 16) != 0 )
    return false;
  return *(_DWORD *)(*a2 + 16LL) == 0;
}
