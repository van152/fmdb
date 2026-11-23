_DWORD *__fastcall sub_143647480(
        __int64 a1,
        _DWORD *a2,
        __int64 *a3,
        __int64 *a4,
        _QWORD *a5,
        __int64 a6,
        __int64 a7,
        __int16 a8,
        int a9)
{
  int v12; // r14d
  __int64 v13; // rdx
  __int64 v14; // r9
  char v15; // r15
  void (__fastcall ***v16)(_QWORD, __int64); // rcx
  bool v17; // r13
  _QWORD *v18; // rbx
  BOOL v20; // ecx
  int v21; // eax
  __int64 v22; // rcx
  __int64 v23; // rax
  __int64 v24; // r8
  __int64 v25; // rax
  __int64 v26; // rcx
  void (__fastcall ***v27)(_QWORD, __int64); // rcx
  __int64 v28; // rcx
  __int64 v29; // rcx
  int v30; // [rsp+50h] [rbp-20h] BYREF
  __int64 v31; // [rsp+58h] [rbp-18h] BYREF
  __int64 v32; // [rsp+60h] [rbp-10h]
  _QWORD v33[9]; // [rsp+68h] [rbp-8h] BYREF

  v33[1] = -2;
  v32 = a1;
  v12 = a9;
  v13 = a7;
  v14 = a6;
  v15 = 1;
  if ( a9 == 1 )
  {
    sub_1407D0F70(a1: v32, a2: (unsigned int)v33, a3: (_DWORD)a5, a4: a6, a5: a7, a6: a8, a7: 0, 0);
    v16 = (void (__fastcall ***)(_QWORD, __int64))v33[0];
    v12 = 0;
    v17 = v33[0] != 0;
    v15 = 1;
    if ( v33[0] != 0 )
    {
      v15 = *(_BYTE *)(v32 + 6);
      if ( _InterlockedDecrement((volatile signed __int32 *)(v33[0] + 8LL)) == 0 )
        (**v16)(a1: v16, a2: 1);
    }
    LOBYTE(v12) = v17;
    v13 = a7;
    v14 = a6;
  }
  if ( *a5 == 0
    || (v18 = (_QWORD *)v13,
        sub_1407D2E60(a1: *a5, a2: (unsigned int)&v30, (_DWORD)a3, (_DWORD)a4, a5: v14, a6: v13, a7: v12),
        v30 != 0) )
  {
    *a2 = 1;
    return a2;
  }
  v20 = v15 == 0;
  *(_DWORD *)(*a3 + 12) = v20 | *(_DWORD *)(*a3 + 12) & 0xFFFFFFFE;
  *(_DWORD *)(*a4 + 12) = v20 | *(_DWORD *)(*a4 + 12) & 0xFFFFFFFE;
  v21 = sub_14082DD60(a1: *v18, a2: 0);
  sub_1407D1180(a1: v32, a2: (unsigned int)v33, a3: (_DWORD)a4, a4: v21, a5: a8, a6: v12);
  v22 = *a4;
  if ( *a4 == v33[0] )
  {
    if ( v22 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v22 + 8)) == 0 )
      (**(void (__fastcall ***)(__int64, __int64))v22)(a1: v22, a2: 1);
    if ( *a4 != 0 )
      goto LABEL_15;
  }
  else
  {
    if ( v22 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v22 + 8)) == 0 )
      (**(void (__fastcall ***)(__int64, __int64))v22)(a1: v22, a2: 1);
    v23 = v33[0];
    *a4 = v33[0];
    if ( v23 != 0 )
    {
LABEL_15:
      v24 = *(unsigned __int8 *)(v32 + 7);
      v25 = *a3;
      v31 = v25;
      if ( v25 != 0 )
        _InterlockedIncrement((volatile signed __int32 *)(v25 + 8));
      sub_141215E40(a1: v33, a2: &v31, a3: v24, a4: -1);
      v26 = *a3;
      if ( *a3 == v33[0] )
      {
        if ( v26 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v26 + 8)) == 0 )
          (**(void (__fastcall ***)(__int64, __int64))v26)(a1: v26, a2: 1);
      }
      else
      {
        if ( v26 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v26 + 8)) == 0 )
          (**(void (__fastcall ***)(__int64, __int64))v26)(a1: v26, a2: 1);
        *a3 = v33[0];
        v33[0] = 0;
      }
      v27 = (void (__fastcall ***)(_QWORD, __int64))v31;
      if ( v31 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v31 + 8)) == 0 )
        (**v27)(a1: v27, a2: 1);
      *a2 = 0;
      return a2;
    }
  }
  v28 = *a3;
  if ( *a3 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v28 + 8)) == 0 )
    (**(void (__fastcall ***)(__int64, __int64))v28)(a1: v28, a2: 1);
  *a3 = 0;
  v29 = *a4;
  if ( *a4 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v29 + 8)) == 0 )
    (**(void (__fastcall ***)(__int64, __int64))v29)(a1: v29, a2: 1);
  *a4 = 0;
  *a2 = 1;
  return a2;
}
