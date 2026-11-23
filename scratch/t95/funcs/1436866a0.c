__int64 __fastcall sub_1436866A0(__int64 a1, unsigned int a2, __int64 a3)
{
  char v6; // al
  __int64 v7; // rax
  __int64 v8; // r8
  unsigned int v9; // eax
  unsigned int v10; // esi
  __int64 v11; // rax
  __int64 v12; // r8
  _QWORD v14[6]; // [rsp+20h] [rbp-10h] BYREF

  v14[2] = -2;
  v14[1] = 0;
  v14[0] = sub_14083D4F0(a1) + 8;
  if ( (*(unsigned __int8 (__fastcall **)(__int64, _QWORD, _QWORD *))(*(_QWORD *)a1 + 16LL))(a1, a2, v14) != 0 )
  {
    v6 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v14[0] + 8LL))(v14[0], v14);
    if ( v6 == 11 )
    {
      v11 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *, _QWORD))(*(_QWORD *)v14[0] + 184LL))(v14[0], v14, 0);
      LOBYTE(v12) = 1;
      v9 = sub_140839A50(v11, a3, v12, 0);
      goto LABEL_7;
    }
    if ( v6 == 10 )
    {
      v7 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *, _QWORD))(*(_QWORD *)v14[0] + 176LL))(v14[0], v14, 0);
      LOBYTE(v8) = 1;
      v9 = sub_140839850(v7, a3, v8, 0);
LABEL_7:
      v10 = v9;
      goto LABEL_8;
    }
  }
  v10 = 0;
LABEL_8:
  (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v14[0] + 16LL))(v14[0], v14);
  return v10;
}
