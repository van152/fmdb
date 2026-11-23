__int64 __fastcall sub_143E8DE60(__int64 a1, __int64 a2, unsigned int a3, int a4)
{
  _BYTE v8[8]; // [rsp+30h] [rbp-20h] BYREF
  _QWORD v9[7]; // [rsp+38h] [rbp-18h] BYREF

  v9[2] = -2;
  (*(void (__fastcall **)(__int64, _BYTE *))(*(_QWORD *)a2 + 144LL))(a2, v8);
  LOBYTE(a1) = (*(__int64 (__fastcall **)(__int64, __int64, _BYTE *, _QWORD, int))(*(_QWORD *)qword_141B5EF38 + 488LL))(
                 qword_141B5EF38,
                 a1,
                 v8,
                 a3,
                 a4);
  (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v9[0] + 16LL))(v9[0], v9);
  return (unsigned int)a1;
}
