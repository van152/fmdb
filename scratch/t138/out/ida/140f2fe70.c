char __fastcall sub_140F2FE70(__int64 a1, _QWORD *a2, __int64 a3)
{
  __int64 v6; // rbx
  __int64 v7; // rbx
  __int64 *v9; // r12
  __int64 v10; // rax
  unsigned __int64 v11; // rcx
  unsigned __int64 v12; // r14
  void (__fastcall ***v13)(_QWORD, __int64); // rcx
  __int64 v14; // r12
  __int64 v15; // r13
  __int64 v16; // rbp
  __int64 v17; // r14
  __int64 v18; // rbx
  unsigned __int64 v19; // rcx
  __int64 v20; // r8
  __int64 v21; // rcx
  __int64 v22; // rbx
  __int64 v23; // rcx
  bool v24; // al
  __int64 v25; // rbp
  __int64 v26; // rbx
  __int64 v27; // rax
  __int64 v28; // r8
  __int64 v29; // rax
  __int64 v30; // rbx
  _DWORD *v31; // rdi
  int v32; // [rsp+30h] [rbp-78h]
  unsigned int v33; // [rsp+4Ch] [rbp-5Ch] BYREF
  _BYTE v34[8]; // [rsp+50h] [rbp-58h] BYREF
  __int64 v35; // [rsp+58h] [rbp-50h] BYREF
  __int64 v36; // [rsp+60h] [rbp-48h]

  v6 = *a2;
  (*(void (__fastcall **)(_QWORD, unsigned int *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v33, a3: 4);
  if ( *(_DWORD *)(v6 + 16) != 0 )
    return 0;
  v7 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 92, a3: 1);
  if ( *(_DWORD *)(v7 + 16) != 0 )
    return 0;
  if ( v33 != 0 )
  {
    v9 = *(__int64 **)(a1 + 128);
    v10 = *v9;
    v11 = (v9[1] - *v9) >> 3;
    if ( v11 < v33 )
    {
      v12 = v33 - 1;
      v35 = 0;
      if ( v11 > v12 )
      {
        v13 = *(void (__fastcall ****)(_QWORD, __int64))(v10 + 8 * v12);
        if ( v13 != nullptr )
          (**v13)(a1: v13, a2: 1);
      }
      sub_14083D020(a1: v9, a2: &v35, a3: v12);
    }
  }
  if ( (*(_BYTE *)(a1 + 92) & 1) != 0 )
  {
    v14 = v33;
    v15 = *(_QWORD *)(a1 + 136);
    if ( (*(_QWORD *)(a1 + 152) - v15) >> 3 < (unsigned __int64)v33 )
    {
      v16 = *(_QWORD *)(a1 + 144);
      v17 = sub_1407E4490(a1: qword_141ABD470, a2: 8LL * v33);
      sub_141758A00(a1: v17, a2: *(_QWORD *)(a1 + 136), a3: *(_QWORD *)(a1 + 144) - *(_QWORD *)(a1 + 136));
      v18 = *(_QWORD *)(a1 + 136);
      if ( v18 != 0 )
      {
        v19 = *(_QWORD *)(a1 + 152) - v18;
        if ( v19 == -1 )
          v19 = *(unsigned int *)(v18 - *(unsigned int *)(qword_141ABD470 + 48));
        if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
          && (v20 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v20) >> 3 > v19)
          && (v21 = *(_QWORD *)(v20 + 8 * v19)) != 0 )
        {
          v22 = v18 - *(unsigned int *)(v21 + 120);
          v36 = v21;
          MEMORY[0x1419475D8](a1: v21 + 32, a2: v22);
          v23 = v36;
          v24 = *(_BYTE *)(v36 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v36 + 64)) != 0;
          if ( !v24 && *(_BYTE *)(v23 + 97) != 0 )
            sub_1412D33C0();
        }
        else
        {
          MEMORY[0x141948990](a1: v18 - *(unsigned int *)(qword_141ABD470 + 48));
        }
      }
      *(_QWORD *)(a1 + 136) = v17;
      *(_QWORD *)(a1 + 144) = v17 + v16 - v15;
      *(_QWORD *)(a1 + 152) = v17 + 8 * v14;
    }
  }
  if ( v33 != 0 )
  {
    v25 = 0;
    do
    {
      v26 = *a2;
      (*(void (__fastcall **)(_QWORD, __int64 *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v35, a3: 1);
      if ( *(_DWORD *)(v26 + 16) != 0 )
        return 0;
      v27 = sub_140F49530(a1: *(unsigned int *)(a1 + 84), a2: (unsigned __int8)v35);
      if ( v27 != 0 )
      {
        LOBYTE(v32) = 1;
        LOBYTE(v28) = 1;
        if ( (*(unsigned __int8 (__fastcall **)(__int64, _QWORD *, __int64, __int64, _DWORD, _DWORD, int, __int64))(*(_QWORD *)v27 + 152LL))(
               a1: v27,
               a2,
               a3: v28,
               a4: a3,
               a5: *(_DWORD *)(a1 + 84),
               a6: v25,
               a7: v32,
               a8: a1) == 0 )
          return 0;
      }
    }
    while ( ++v25 < (unsigned __int64)v33 );
  }
  v29 = *(_QWORD *)(a1 + 8);
  if ( v29 != *(_QWORD *)(a1 + 16) )
    *(_QWORD *)(a1 + 16) = v29;
  sub_140FFAFD0(a1: &v35, a2, a3: a1 + 8, a4: v34);
  if ( (_DWORD)v35 != 0 )
    return 0;
  v30 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 88, a3: 1);
  if ( *(_DWORD *)(v30 + 16) != 0 )
    return 0;
  v31 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v31 + 40LL))(a1: v31, a2: a1 + 80, a3: 4);
  if ( v31[4] != 0 )
    return 0;
  *(_WORD *)(a1 + 89) = 1;
  return 1;
}
