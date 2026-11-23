// THUNK ALIAS -> sub_1436846E0 (jmp:0x1407eb170->0x1436846e0)
char __fastcall sub_1436846E0(__int64 a1, __int64 a2, _QWORD *a3)
{
  __int64 v3; // rax
  unsigned __int64 v7; // rax
  __int64 v8; // r12
  __int64 i; // rbx
  unsigned int v10; // esi
  __int64 v11; // rcx
  __int64 v12; // rax
  _QWORD v14[10]; // [rsp+20h] [rbp-10h] BYREF

  v14[2] = -2;
  v3 = a3[1] - *a3;
  if ( v3 != 0 )
  {
    v7 = v3 >> 3;
    v8 = 1;
    if ( v7 >= 2 )
      v8 = v7;
    for ( i = 0; i != v8; ++i )
    {
      v10 = (*(__int64 (__fastcall **)(_QWORD))(***(_QWORD ***)(*a3 + 8 * i) + 80LL))(**(_QWORD **)(*a3 + 8 * i));
      v12 = sub_14083D4F0(v11);
      v14[1] = 0;
      v14[0] = v12 + 8;
      if ( (*(unsigned __int8 (__fastcall **)(__int64, _QWORD, _QWORD *))(*(_QWORD *)a2 + 16LL))(a2, v10, v14) != 0
        && (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v14[0] + 8LL))(v14[0], v14) != 0 )
      {
        (*(void (__fastcall **)(__int64, _QWORD, _QWORD *))(*(_QWORD *)a1 + 24LL))(a1, v10, v14);
      }
      (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v14[0] + 16LL))(v14[0], v14);
    }
  }
  return 1;
}
