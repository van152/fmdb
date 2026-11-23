char __fastcall sub_144523940(_DWORD *a1, int a2, __int64 *a3)
{
  __int64 v4; // rcx
  __int64 v5; // rax
  __int64 v6; // rcx
  __int64 v7; // rax
  __int64 v8; // rax
  __int64 v9; // rcx
  __int64 v10; // rdx
  __int64 v11; // rcx
  void (__fastcall ***v12)(_QWORD, __int64); // rcx
  __int64 v14; // [rsp+30h] [rbp-20h] BYREF
  __int64 v15; // [rsp+38h] [rbp-18h] BYREF
  __int64 v16; // [rsp+40h] [rbp-10h] BYREF
  __int64 v17; // [rsp+48h] [rbp-8h]
  __int64 v18; // [rsp+50h] [rbp+0h]

  v18 = -2;
  if ( a2 != 1382965613 )
    return sub_140FE3F20(a1, a2, a3);
  (*(void (__fastcall **)(_DWORD *, __int64 *))(*(_QWORD *)a1 + 200LL))(a1, &v15);
  sub_14081AF20(v15, (unsigned int)&v14, (unsigned int)&qword_141B59EE0, 0, 0, 0);
  v5 = sub_14083D4F0(v4);
  v17 = 0;
  v6 = v14;
  if ( v14 != 0 )
    _InterlockedIncrement((volatile signed __int32 *)(v14 - 4));
  v17 = v6;
  v7 = v5 + 136;
  v16 = v7;
  if ( &v16 != a3 )
  {
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
    v8 = v16;
    v9 = v17;
    a3[1] = v17;
    *a3 = v8;
    v7 = sub_14083D4F0(v9) + 8;
    v17 = 0;
    v16 = v7;
  }
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v7 + 16LL))(v7, &v16);
  v11 = v14;
  if ( v14 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v14 - 4)) == 0 )
    sub_1412EC9A0(v11 - 4, v10);
  v12 = (void (__fastcall ***)(_QWORD, __int64))v15;
  if ( v15 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v15 + 8)) == 0 )
    (**v12)(v12, 1);
  return 1;
}
