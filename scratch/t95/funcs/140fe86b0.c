// THUNK ALIAS -> sub_143E39180 (jmp:0x140fe86b0->0x143e39180)
__int64 __fastcall sub_143E39180(__int64 a1)
{
  __int64 result; // rax
  __int64 v2[2]; // [rsp+20h] [rbp-30h] BYREF
  int v3; // [rsp+30h] [rbp-20h] BYREF
  _QWORD v4[5]; // [rsp+38h] [rbp-18h] BYREF

  v4[2] = -2;
  if ( a1 != 0 )
  {
    (*(void (__fastcall **)(__int64, int *))(*(_QWORD *)a1 + 144LL))(a1, &v3);
    sub_140FEAD00(&v3, v2);
    sub_140835380(&qword_141B60C30, 1416914273, v2);
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v2[0] + 16LL))(v2[0], v2);
    return (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v4[0] + 16LL))(v4[0], v4);
  }
  return result;
}
