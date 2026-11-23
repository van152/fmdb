// THUNK ALIAS -> sub_14376F1B0 (jmp:0x140833970->0x14376f1b0)
void __fastcall sub_14376F1B0(__int64 *a1)
{
  __int64 v1; // rdi
  __int64 v3; // r15
  void (__fastcall *v4)(__int64, _QWORD *); // r12
  _QWORD *v5; // rsi
  __int64 v6; // rbx

  v1 = *a1;
  if ( *a1 != 0 )
  {
    v3 = a1[1];
    if ( v1 != v3 )
    {
      v4 = (void (__fastcall *)(__int64, _QWORD *))MEMORY[0x1419475D8];
      do
      {
        v5 = *(_QWORD **)(v1 + 8);
        if ( v5 != nullptr )
        {
          (*(void (__fastcall **)(_QWORD, _QWORD))(*(_QWORD *)*v5 + 16LL))(*v5, *(_QWORD *)(v1 + 8));
          v6 = sub_140836BC0();
          v4(v6 + 32, v5);
          if ( (*(_BYTE *)(v6 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v6 + 64)) == 0)
            && *(_BYTE *)(v6 + 97) != 0 )
          {
            sub_1412D33C0(v6);
          }
        }
        v1 += 16;
      }
      while ( v1 != v3 );
      v1 = *a1;
    }
    sub_1407E4890(qword_141ABD470, v1, a1[2] - v1);
    a1[2] = 0;
    a1[1] = 0;
    *a1 = 0;
  }
}
