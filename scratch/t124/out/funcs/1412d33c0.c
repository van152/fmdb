__int64 __fastcall sub_1412D33C0(__int64 a1)
{
  __int64 v1; // rsi
  __int64 result; // rax
  bool v3; // zf
  int v4; // eax
  __int64 v5; // rbx
  __int64 v6; // rcx
  __int64 v7; // rax
  unsigned __int64 v8; // rsi
  __int64 v9; // rdi
  unsigned __int64 v10; // rcx
  __int64 v11; // rax
  __int64 v12; // rcx
  __int64 v13; // rsi
  signed __int32 v14; // ebx
  signed __int32 v15; // ebx
  __int64 v16; // rsi
  __int64 v17; // rcx
  __int64 v18; // rcx
  unsigned __int64 v19; // rax
  __int64 v20; // r15
  __int64 v21; // r13
  __int64 v22; // rax
  signed __int32 v23; // esi
  __int64 v24; // rdi
  __int64 v25; // rsi
  __int64 v26; // rdi
  unsigned __int64 v27; // r12
  unsigned __int64 v28; // r14
  __int64 v29; // rcx
  __int64 v30; // rax
  unsigned __int64 v31; // rbx
  _QWORD *v32; // rdi
  _QWORD *v33; // rsi
  __int64 v34; // rbx
  void (__fastcall *v35)(__int64, _QWORD); // r14
  _QWORD *v36; // rdi
  _QWORD *v37; // rsi
  void (__fastcall *v38)(__int64, _QWORD); // r14
  __int64 v39; // rcx
  __int64 v40; // rcx
  __int64 *v41; // rdi
  __int64 *v42; // rsi
  void (__fastcall *v43)(__int64); // r14
  void (__fastcall *v44)(__int64); // r15
  __int64 v45; // rcx
  __int64 v46; // [rsp+20h] [rbp-60h] BYREF
  __int64 v47; // [rsp+28h] [rbp-58h]
  __int64 v48; // [rsp+30h] [rbp-50h]
  __int64 v49; // [rsp+38h] [rbp-48h]
  __int128 v50; // [rsp+40h] [rbp-40h] BYREF
  unsigned __int64 v51; // [rsp+50h] [rbp-30h]
  __int128 v52; // [rsp+60h] [rbp-20h]
  unsigned __int64 v53; // [rsp+70h] [rbp-10h]
  __int64 v54; // [rsp+78h] [rbp-8h]
  __int64 v55; // [rsp+80h] [rbp+0h]

  v55 = -2;
  v1 = a1;
  result = (unsigned __int8)_InterlockedCompareExchange8((volatile signed __int8 *)(a1 + 73), 1, 0);
  if ( (_BYTE)result == 0 )
  {
    v50 = 0;
    v51 = 0;
    v3 = *(_BYTE *)(a1 + 72) == 0;
    v54 = a1;
    if ( !v3 )
    {
      v4 = *(_DWORD *)(a1 + 60) - *(_DWORD *)(a1 + 64);
      if ( v4 != 0 )
      {
        if ( v4 < 0 )
          ((void (__noreturn *)(void))sub_1400526C0)();
        v5 = v4;
        v6 = 8LL * v4;
        if ( (unsigned int)v4 < 0x200 )
        {
          v8 = sub_141750CC0(v6);
        }
        else
        {
          v7 = sub_141750CC0(v6 + 39);
          v8 = (v7 + 39) & 0xFFFFFFFFFFFFFFE0uLL;
          *(_QWORD *)(v8 - 8) = v7;
        }
        v9 = v50;
        sub_141758A00();
        if ( (_QWORD)v50 != 0 )
        {
          if ( v51 - (unsigned __int64)v50 >= 0x1000 )
          {
            if ( (unsigned __int64)(v50 - 8 - *(_QWORD *)(v50 - 8)) >= 0x20 )
              goto LABEL_86;
            v9 = *(_QWORD *)(v50 - 8);
          }
          sub_141750D04(v9);
        }
        *(_QWORD *)&v50 = v8;
        *((_QWORD *)&v50 + 1) = v8;
        v51 = v8 + 8 * v5;
        v1 = v54;
      }
    }
    v48 = v1 + 32;
    v11 = MEMORY[0x1419475D0](v1 + 32);
    if ( v11 != 0 && *(_BYTE *)(v1 + 72) != 0 )
      _InterlockedIncrement((volatile signed __int32 *)(v1 + 64));
    v12 = 0;
    v49 = 0;
    v13 = v54;
    while ( 1 )
    {
      v46 = v11;
      if ( v11 == 0 )
        break;
      if ( *((_QWORD *)&v50 + 1) == v51 )
      {
        sub_1407E4D40(&v50, *((_QWORD *)&v50 + 1), &v46);
      }
      else
      {
        **((_QWORD **)&v50 + 1) = v11;
        *((_QWORD *)&v50 + 1) += 8LL;
      }
      v15 = _InterlockedExchangeAdd((volatile signed __int32 *)(v13 + 60), 0xFFFFFFFF);
      v11 = MEMORY[0x1419475D0](v48);
      if ( v11 != 0 && *(_BYTE *)(v13 + 72) != 0 )
        _InterlockedIncrement((volatile signed __int32 *)(v13 + 64));
      v14 = v15 - 1;
      v12 = v14;
      v49 = v14;
    }
    v52 = 0;
    v53 = 0;
    v16 = *(int *)(v54 + 56);
    if ( *(_DWORD *)(v54 + 56) != 0 )
    {
      if ( (int)v16 < 0 )
        goto LABEL_87;
      v17 = 8 * v16;
      if ( (unsigned int)v16 < 0x200 )
      {
        v19 = sub_141750CC0(v17);
      }
      else
      {
        v18 = sub_141750CC0(v17 + 39);
        v19 = (v18 + 39) & 0xFFFFFFFFFFFFFFE0uLL;
        *(_QWORD *)(v19 - 8) = v18;
      }
      *(_QWORD *)&v52 = v19;
      *((_QWORD *)&v52 + 1) = v19;
      v53 = v19 + 8 * v16;
    }
    v20 = v54 + 16;
    v21 = MEMORY[0x1419475D0](v54 + 16);
    v22 = 0;
    v47 = v20;
    while ( v21 != 0 )
    {
      v24 = *((_QWORD *)&v52 + 1);
      if ( *((_QWORD *)&v52 + 1) == v53 )
      {
        v25 = v52;
        v26 = *((_QWORD *)&v52 + 1) - v52;
        v27 = (__int64)(*((_QWORD *)&v52 + 1) - v52) >> 3;
        v28 = v27 + (v27 >> 1);
        if ( v28 <= v27 + 1 )
          v28 = (v26 >> 3) + 1;
        if ( v27 > 0x1FFFFFFFFFFFFFFFLL - (v27 >> 1) )
          v28 = 0x1FFFFFFFFFFFFFFFLL;
        if ( v28 >> 61 != 0 )
          sub_1400DAC30(0x1FFFFFFFFFFFFFFFLL);
        v29 = 8 * v28;
        if ( v28 < 0x200 )
        {
          if ( v28 != 0 )
            v31 = sub_141750CC0(v29);
          else
            v31 = 0;
        }
        else
        {
          if ( v28 >= 0x1FFFFFFFFFFFFFFCLL )
            sub_1400DAC30(v29);
          v30 = sub_141750CC0(v29 + 39);
          v31 = (v30 + 39) & 0xFFFFFFFFFFFFFFE0uLL;
          *(_QWORD *)(v31 - 8) = v30;
        }
        *(_QWORD *)(v31 + 8 * v27) = v21;
        sub_141758A00();
        if ( v25 != 0 )
        {
          if ( (unsigned __int64)v26 >= 0x1000 )
          {
            if ( (unsigned __int64)(v25 - 8 - *(_QWORD *)(v25 - 8)) >= 0x20 )
              goto LABEL_86;
            v25 = *(_QWORD *)(v25 - 8);
          }
          sub_141750D04(v25);
        }
        *(_QWORD *)&v52 = v31;
        *((_QWORD *)&v52 + 1) = v31 + 8 * (v27 + 1);
        v53 = v31 + 8 * v28;
        v20 = v47;
      }
      else
      {
        **((_QWORD **)&v52 + 1) = v21;
        *((_QWORD *)&v52 + 1) = v24 + 8;
      }
      v23 = _InterlockedExchangeAdd((volatile signed __int32 *)(v54 + 56), 0xFFFFFFFF);
      v21 = MEMORY[0x1419475D0](v20);
      v22 = v23 - 1;
    }
    v49 |= v22;
    if ( v49 != 0 || *(_DWORD *)(v54 + 60) != 0 )
    {
      v32 = *((_QWORD **)&v50 + 1);
      v33 = (_QWORD *)v50;
      v34 = v54;
      if ( (_QWORD)v50 != *((_QWORD *)&v50 + 1) )
      {
        v35 = (void (__fastcall *)(__int64, _QWORD))MEMORY[0x1419475D8];
        MEMORY[0x1419475D8](v48, *(_QWORD *)v50);
        while ( 1 )
        {
          if ( *(_BYTE *)(v34 + 72) != 0 )
            _InterlockedDecrement((volatile signed __int32 *)(v34 + 64));
          _InterlockedIncrement((volatile signed __int32 *)(v34 + 60));
          if ( ++v33 == v32 )
            break;
          v35(v48, *v33);
        }
      }
      v36 = *((_QWORD **)&v52 + 1);
      v37 = (_QWORD *)v52;
      if ( (_QWORD)v52 != *((_QWORD *)&v52 + 1) )
      {
        v38 = (void (__fastcall *)(__int64, _QWORD))MEMORY[0x1419475D8];
        do
        {
          v38(v20, *v37);
          _InterlockedIncrement((volatile signed __int32 *)(v34 + 56));
          ++v37;
        }
        while ( v37 != v36 );
      }
    }
    else
    {
      v34 = v54;
      if ( *(_BYTE *)(v54 + 72) != 0 )
        _InterlockedAdd((volatile signed __int32 *)(v54 + 64), -(int)((*((_QWORD *)&v50 + 1) - (_QWORD)v50) >> 3));
      v41 = *((__int64 **)&v52 + 1);
      v42 = (__int64 *)v52;
      if ( (_QWORD)v52 != *((_QWORD *)&v52 + 1) )
      {
        v43 = (void (__fastcall *)(__int64))MEMORY[0x141948960];
        v44 = (void (__fastcall *)(__int64))MEMORY[0x141948990];
        do
        {
          v45 = *v42;
          if ( (*(_DWORD *)(v34 + 8) & 0xFFF000u) < 0x2001 )
            v44(v45);
          else
            v43(v45);
          ++v42;
          v34 = v54;
        }
        while ( v42 != v41 );
      }
    }
    result = *(unsigned __int8 *)(v34 + 73);
    *(_BYTE *)(v34 + 73) = 0;
    v39 = v52;
    if ( (_QWORD)v52 == 0 )
      goto LABEL_70;
    if ( v53 - (unsigned __int64)v52 < 0x1000 )
    {
LABEL_69:
      result = sub_141750D04(v39);
LABEL_70:
      v40 = v50;
      if ( (_QWORD)v50 == 0 )
        return result;
      if ( v51 - (unsigned __int64)v50 < 0x1000 )
        return sub_141750D04(v40);
      v10 = v50 - 8 - *(_QWORD *)(v50 - 8);
      if ( v10 < 0x20 )
      {
        v40 = *(_QWORD *)(v50 - 8);
        return sub_141750D04(v40);
      }
      goto LABEL_86;
    }
    v10 = v52 - 8 - *(_QWORD *)(v52 - 8);
    if ( v10 < 0x20 )
    {
      v39 = *(_QWORD *)(v52 - 8);
      goto LABEL_69;
    }
LABEL_86:
    MEMORY[0x1419488E8](v10);
LABEL_87:
    sub_1400526C0(v12);
  }
  return result;
}
