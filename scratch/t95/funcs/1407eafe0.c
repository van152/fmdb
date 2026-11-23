// THUNK ALIAS -> sub_1436843A0 (jmp:0x1407eafe0->0x1436843a0)
char __fastcall sub_1436843A0(__int64 a1, __int64 *a2, __int64 *a3)
{
  __int64 v6; // r12
  __int64 v7; // rdi
  unsigned __int64 v8; // rsi
  __int64 v9; // rax
  unsigned __int64 v10; // rdx
  unsigned __int64 v11; // rcx
  __int64 v12; // r12
  __int64 i; // rdi
  unsigned int v14; // esi
  __int64 v15; // rcx
  __int64 v16; // rax
  __int64 v18[10]; // [rsp+20h] [rbp-10h] BYREF

  v18[2] = -2;
  v6 = *a3;
  v7 = a3[1];
  v8 = (v7 - *a3) >> 3;
  v9 = *a2;
  v10 = v8 + ((a2[1] - *a2) >> 4);
  v11 = (a2[2] - v9) >> 4;
  if ( v11 < v10 )
  {
    if ( v10 >> 60 != 0 )
      sub_1400526C0(v11);
    sub_140837DD0(a2, v10);
  }
  if ( v7 != v6 )
  {
    v12 = 1;
    if ( v8 >= 2 )
      v12 = v8;
    for ( i = 0; i != v12; ++i )
    {
      v14 = (*(__int64 (__fastcall **)(_QWORD))(***(_QWORD ***)(*a3 + 8 * i) + 80LL))(**(_QWORD **)(*a3 + 8 * i));
      v16 = sub_14083D4F0(v15);
      v18[1] = 0;
      v18[0] = v16 + 8;
      if ( (*(unsigned __int8 (__fastcall **)(__int64, _QWORD, __int64 *))(*(_QWORD *)a1 + 16LL))(a1, v14, v18) != 0 )
        sub_140835380(a2, v14, v18);
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v18[0] + 16LL))(v18[0], v18);
    }
  }
  return 1;
}
